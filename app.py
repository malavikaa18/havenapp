from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safezone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class SOSAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_sos", methods=["POST"])

def send_sos():
    data = request.json
    if not all(key in data for key in ["user_email", "latitude", "longitude"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_alert = SOSAlert(
        user_email=data["user_email"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({"message": "SOS Alert Sent!"}), 201

@app.route("/get_sos_alerts", methods=["GET"])
def get_sos_alerts():
    alerts = SOSAlert.query.all()
    return jsonify([{
        "user_email": alert.user_email,
        "latitude": alert.latitude,
        "longitude": alert.longitude,
        "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for alert in alerts])

@app.route("/add_contact", methods=["POST"])
def add_contact():
    data = request.json
    if not all(key in data for key in ["user_email", "contact_name", "contact_number"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_contact = EmergencyContact(
        user_email=data["user_email"],
        contact_name=data["contact_name"],
        contact_number=data["contact_number"]
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({"message": "Emergency Contact Added!"}), 201

@app.route("/get_contacts", methods=["GET"])
def get_contacts():
    contacts = EmergencyContact.query.all()
    return jsonify([{
        "user_email": contact.user_email,
        "contact_name": contact.contact_name,
        "contact_number": contact.contact_number
    } for contact in contacts])

if __name__ == "__main__":
    app.run(debug=True)
