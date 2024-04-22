"""Patient API Controller"""

from flask import Flask
from patient_db import PatientDB
from flask import jsonify, request
from patient import Patient


class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)


    """
    TODO:
    Implement the following methods,
    use the self.patient_db object to interact with the database.

    Every method in this class should return a JSON response with status code
    Status code should be 200 if the operation was successful,
    Status code should be 400 if there was a client error,
    """

    def create_patient(self):
        data = request.json
        if not data:
            return jsonify({"error" : "No data provided"}), 400
        
        patient_id = self.patient_db.insert_patient(data)
        if patient_id is None:
            return jsonify({"error" : "Failed to create patient"}), 400
        
        new_patient = self.patient_db.fetch_patient_id_by_name(data["patient_name"])

        return jsonify(new_patient), 200
    

    def get_patients(self):

        search_name = request.args.get("search_name")
        if search_name == None:
            patients = self.patient_db.select_all_patients()
            if not patients:
                return jsonify({"error" : "Database is empty "}), 200
            return jsonify(patients), 200
        
        else:
            patient_ids = self.patient_db.fetch_patient_id_by_name(search_name)
            if not patient_ids:
                return jsonify({"message" : "No patients with that name"}), 200
            
            patients = []
            for patient_id in patient_ids:
                patient = self.patient_db.select_patient(patient_id["patient_id"])
                patients.append(patient)
            return jsonify(patient), 200

    def get_patient(self, patient_id):
        patient = self.patient_db.select_patient(patient_id)
        if patient is None:
            return jsonify({"error" : "Patient not found"}), 400
        return jsonify(patient), 200
       
    def update_patient(self, patient_id):
        data = request.json
        if not data:
            return jsonify({"error" : "No data provided"}), 400

        affected_rows = self.patient_db.update_patient(patient_id, data)
        if affected_rows is None:
            return jsonify({"error" : "Failed to update patient"}), 400
        return jsonify({"message" : "Patient updated successfully"}), 200
    

    def delete_patient(self, patient_id):
        affected_rows = self.patient_db.delete_patient(patient_id)
        if affected_rows is None:
            return jsonify({"error" : "Failed to delete patient"}),400
        return jsonify({"message" : "Patient deleted successfully"}), 200

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()


PatientAPIController()
