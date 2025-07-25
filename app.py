from flask import Flask
from controller.patient_routes import patient_bp
from controller.appointment_routes import appointment_bp


app = Flask(__name__)
app.register_blueprint(patient_bp)
app.register_blueprint(appointment_bp)


if __name__ == "__main__":
    app.run(debug=True)
