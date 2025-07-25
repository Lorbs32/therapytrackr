from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

patient_bp = Blueprint("client_bp", __name__)

patient = MongoClient("mongodb+srv://lorbs32:hbstudent@cluster1.7yqbvki.mongodb.net/")
db = patient["therapytrackr"]
patients_collection = db["patients"]


# Home page
@patient_bp.route("/")
def home():
    return "Welcome to TherapyTrackr API"


# GET request to return all patients
@patient_bp.route("/patients", methods=["GET"])
def get_patients():
    patients = list(patients_collection.find())
    for p in patients:
        p["_id"] = str(p["_id"])
    return jsonify(patients)


# GET request to return patient by id
@patient_bp.route("/patients/<string:patient_id>", methods=["GET"])
def get_patient(patient_id):
    try:
        patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return jsonify(patient)
        return jsonify({"error": "Patient not found"}), 404
    except Exception:
        return jsonify({"error": "invalid ID format"}), 400


# POST request to add a new patient
@patient_bp.route("/patients", methods=["POST"])
def add_patient():
    data = request.get_json()
    new_patient = {
        "name": data.get("name"),
        "age": data.get("age"),
        "condition": data.get("condition"),
    }
    result = patients_collection.insert_one(new_patient)
    new_patient["_id"] = str(result.inserted_id)
    return jsonify(new_patient), 201


# PUT request to update patient
@patient_bp.route("/patients/<string:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    updated_data = request.get_json()
    result = patients_collection.update_one(
        {"_id": ObjectId(patient_id)}, {"$set": updated_data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Patient not found"}), 404
    updated_patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    updated_patient["_id"] = str(updated_patient["_id"])
    return jsonify(updated_patient)


# DELETE request to remove a patient
@patient_bp.route("/patients/<string:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    result = patients_collection.delete_one({"_id": ObjectId(patient_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify({"message": f"Patient with ID {patient_id} deleted."})


# MongoDB test connection
@patient_bp.route("/test-mongo")
def test_mongo_connection():
    try:
        # Try inserting a temporary document
        test_doc = {"message": "Hello from MongoDB!"}
        result = patients_collection.insert_one(test_doc)

        # Then immediately find it
        inserted_doc = patients_collection.find_one({"_id": result.inserted_id})

        # Clean up (optional in dev)
        patients_collection.delete_one({"_id": result.inserted_id})

        inserted_doc["_id"] = str(inserted_doc["_id"])

        return jsonify({"success": True, "document": str(inserted_doc)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
