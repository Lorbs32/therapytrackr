from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data
patients = [
    {"id": 1, "name": "Alice Johnson", "age": 34, "condition": "Diabetes"},
    {"id": 2, "name": "Bob Smith", "age": 45, "condition": "Hypertension"},
    {"id": 3, "name": "Carol Lee", "age": 29, "condition": "Asthma"}
]

# Home page
@app.route('/')
def home():
    return "Welcome to PatientTrackr API"

# GET request to return all patients
@app.route('/patients')
def get_patients():
    return jsonify(patients)

# GET request to return patient by id
@app.route('/patients/<int:patient_id>')
def get_patient(patient_id):
    patient = next((p for p in patients if p['id'] == patient_id), None)
    if patient:
        return jsonify(patient)
    return jsonify({"error": "Patient not found"}), 404

# GET request to add a new patient
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    new_id = max(p['id'] for p in patients) + 1 if patients else 1
    new_patient = {
        "id": new_id,
        "name": data.get("name"),
        "age": data.get("age"),
        "condition": data.get("condition")
    }
    patients.append(new_patient)
    return jsonify(new_patient), 201

# PUT request to update patient
@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    updated_data = request.get_json()
    for patient in patients:
        if patient['id'] == patient_id:
            patient.update(updated_data)
            return jsonify(patient)
    return jsonify({"error": "Patient not found"}), 404

# DELETE request to remove a patient
@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    global patients
    new_list = [p for p in patients if p['id'] != patient_id]
    if len(new_list) == len(patients):
        return jsonify({"error": "Patient not found"}), 404
    patients = new_list
    return jsonify({"message": f"Patient with ID {patient_id} deleted."})

if __name__ == '__main__':
    app.run(debug=True)

