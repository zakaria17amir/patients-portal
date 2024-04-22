"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""

import uuid, requests, random
from datetime import datetime
from patient_db import PatientDB
from patient_db_config import PATIENTS_TABLE
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL

class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())
        self.patient_name = name
        self.patient_gender = gender
        self.patient_age = age
        self.patient_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_checkout = None
        self.patient_ward = None
        self.patient_room = None

    def get_id(self):
        return self.patient_id
    def get_name(self):
        return self.patient_name
    def get_age(self):
        return self.patient_age
    def get_gender(self):
        return self.patient_gender
    
    def set_room(self, room): 
        print()
        if any(str(room) in room_numbers for room_numbers in ROOM_NUMBERS.values()):
            self.patient_room = str(room)

    def set_ward(self, ward):
        if ward in WARD_NUMBERS:
            self.patient_ward = ward

    def get_room(self):
        return self.patient_room
    def get_ward(self):
        return self.patient_ward
        
    def commit(self):
        patient_data = {
            "patient_id":self.patient_id,
            "patient_name" : self.patient_name,
            "patient_age" : self.patient_age,
            "patient_gender" : self.patient_gender,
            "patient_checkin" :self.patient_checkin,
            "patient_checkout" : self.patient_checkout,
            "patient_ward" : self.patient_ward,
            "patient_room" : self.patient_room
        }

        url = f"{API_CONTROLLER_URL}"
        url_n = f"{API_CONTROLLER_URL}/patients"
        url_a = f"{API_CONTROLLER_URL}/patient/{self.patient_id}"
        response = requests.get(url_n)
        response_in_json = response.json()
        ids = [patient['patient_id'] for patient in response_in_json if patient['patient_id'] == self.patient_id]
        print(ids)
        if self.patient_id in ids:
            response = requests.put(url_a, json=patient_data)
            # response.raise_for_status()
            if response.status_code == 200:
                print("patient commited successful")
            else:
                print("patient commit unsuccesfull")

        else:
            response = requests.post(url_n, json=patient_data)
            # response.raise_for_status()
            if response.status_code == 200:
                print("patient commited successful")
            else:
                print("patient commit unsuccesfull")
        
       
