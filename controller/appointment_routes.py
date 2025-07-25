from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

appointment_bp = Blueprint("appointment_bp", __name__)

client = MongoClient("mongodb+srv://lorbs32:hbstudent@cluster1.7yqbvki.mongodb.net/")
db = client["therapytrackr"]
appointment_collection = db["appointments"]


# POST request to add a new appointment
@appointment_bp.route("/appointments", methods=["POST"])
def add_appointment():
    data = request.get_json()
    new_appointment = {
        "patient_id": data.get("patient_id"),
        "doctor_id": data.get("doctor_id"),
        "date": data.get("date"),
        "time": data.get("time"),
        "notes": data.get("notes"),
    }
    result = appointment_collection.insert_one(new_appointment)
    new_appointment["_id"] = str(result.inserted_id)
    return jsonify(new_appointment), 201


# GET request to return all appointments
@appointment_bp.route("/appointments", methods=["Get"])
def get_appointments():
    appointments = list(appointment_collection.find())
    for each_appointment in appointments:
        each_appointment["_id"] = str(each_appointment["_id"])
    return jsonify(appointments)


# GET request to return single appointment
@appointment_bp.route("/appointments/<string:appointment_id>", methods=["GET"])
def get_appointment(appointment_id):
    appointment = appointment_collection.find_one({"_id": ObjectId(appointment_id)})
    if appointment:
        appointment["_id"] = str(appointment["_id"])
        return jsonify(appointment)
    return jsonify({"error": "Appointment not found"}), 404


# PUT request to update existing appointment
@appointment_bp.route("/appointments/<string:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    # gets updated fields from request body
    updated_data = request.get_json()
    # update entry in MongoDB where id matches
    result = appointment_collection.update_one(
        {"_id": ObjectId(appointment_id)}, {"$set": updated_data}
    )
    # if not found - return error
    if result.matched_count == 0:
        return jsonify({"error": "Appointment not found"}), 404
    # otherwise create updated appointment and convert id to a string
    updated_appointment = appointment_collection.find_one(
        {"_id": ObjectId(appointment_id)}
    )
    updated_appointment["_id"] = str(updated_appointment["_id"])
    return jsonify(updated_appointment)


# DELETE request to remove an appointment by id
@appointment_bp.route("/appointments/<string:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    result = appointment_collection.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(
        {"message": f"Appointment with ID {appointment_id} was successfully deleted."}
    )
