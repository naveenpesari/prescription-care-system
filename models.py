from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    common_dosage = db.Column(db.String(50))

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    raw_ocr_text = db.Column(db.Text)
    image_path = db.Column(db.String(255))

    items = db.relationship('PrescriptionItem', backref='prescription', lazy=True)

class PrescriptionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    matched_confidence = db.Column(db.Float)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    duration_days = db.Column(db.Integer)

    medicine = db.relationship('Medicine')
    dose_logs = db.relationship('DoseLog', backref='prescription_item', lazy=True)

class DoseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescription_item_id = db.Column(db.Integer, db.ForeignKey('prescription_item.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')