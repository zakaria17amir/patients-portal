#!/bin/bash

patient_name="test-patient_2"
curl -X GET 127.0.0.1:5000/patients?search_name=$patient_name