from app import app
from models import db, Medicine

sample_medicines = [
    {"name": "Paracetamol", "common_dosage": "500mg"},
    {"name": "Amoxicillin", "common_dosage": "250mg"},
    {"name": "Ibuprofen", "common_dosage": "400mg"},
    {"name": "Cetirizine", "common_dosage": "10mg"},
    {"name": "Metformin", "common_dosage": "500mg"},
    {"name": "Amlodipine", "common_dosage": "5mg"},
    {"name": "Azithromycin", "common_dosage": "500mg"},
    {"name": "Omeprazole", "common_dosage": "20mg"},
    {"name": "Pantoprazole", "common_dosage": "40mg"},
    {"name": "Dolo 650", "common_dosage": "650mg"},
]

with app.app_context():
    for med in sample_medicines:
        exists = Medicine.query.filter_by(name=med["name"]).first()
        if not exists:
            new_medicine = Medicine(name=med["name"], common_dosage=med["common_dosage"])
            db.session.add(new_medicine)
    db.session.commit()
    print("Sample medicines added successfully!")