from flask import Flask, render_template, request, redirect
from models import db, Medicine, Prescription, PrescriptionItem, DoseLog
import os
import pytesseract
from PIL import Image
from datetime import datetime, timedelta
from matcher import find_best_match, extract_candidate_words
from parser import parse_dosage_info
from interactions import check_interactions

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prescription.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('prescription_image')

    if not file:
        return "No file uploaded!"

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)

    # Run OCR on the uploaded image
    image = Image.open(save_path)
    extracted_text = pytesseract.image_to_string(image)

    # Get all medicine names from database
    all_medicines = Medicine.query.all()
    medicine_names = [m.name for m in all_medicines]

    # Break OCR text into lines, clean them up
    lines = extracted_text.split('\n')
    lines = [l.strip() for l in lines if len(l.strip()) > 3]

    # Create a new Prescription record
    new_prescription = Prescription(
        raw_ocr_text=extracted_text,
        image_path=save_path
    )
    db.session.add(new_prescription)
    db.session.commit()

    # Try matching each line, parse dosage info, save to database
    matches_found = []
    seen = set()

    for line in lines:
        candidates = extract_candidate_words(line)
        best_overall_match = None
        best_overall_confidence = 0

        for candidate in candidates:
            best_match, distance, confidence = find_best_match(candidate, medicine_names)
            if confidence > best_overall_confidence:
                best_overall_confidence = confidence
                best_overall_match = best_match

        best_match = best_overall_match
        confidence = best_overall_confidence

        if confidence >= 0.6 and best_match not in seen:
            dosage_info = parse_dosage_info(line)

            medicine_obj = Medicine.query.filter_by(name=best_match).first()

            new_item = PrescriptionItem(
                prescription_id=new_prescription.id,
                medicine_id=medicine_obj.id,
                matched_confidence=confidence,
                dosage=dosage_info["frequency"] or "Not specified",
                frequency=dosage_info["frequency"] or "Not specified",
                duration_days=dosage_info["duration_days"] or 0
            )
            db.session.add(new_item)
            db.session.commit()

            create_dose_logs(new_item, dosage_info)

            matches_found.append({
                "original": line,
                "matched": best_match,
                "confidence": confidence,
                "frequency": dosage_info["frequency"],
                "food_timing": dosage_info["food_timing"],
                "duration_days": dosage_info["duration_days"]
            })
            seen.add(best_match)

    # Check for drug interactions among matched medicines
    matched_names = [m["matched"] for m in matches_found]
    interaction_warnings = check_interactions(matched_names)

    return render_template('result.html',
                            filename=file.filename,
                            extracted_text=extracted_text,
                            matches=matches_found,
                            warnings=interaction_warnings)


def create_dose_logs(prescription_item, dosage_info):
    duration = dosage_info["duration_days"] or 1
    frequency = dosage_info["frequency"] or ""

    time_map = {
        "Morning": 8,
        "Afternoon": 13,
        "Evening": 18,
        "Night": 21
    }

    times_today = []
    for time_word, hour in time_map.items():
        if time_word.lower() in frequency.lower():
            times_today.append(hour)

    if not times_today:
        if "once" in frequency.lower():
            times_today = [9]
        elif "twice" in frequency.lower():
            times_today = [9, 21]
        elif "thrice" in frequency.lower():
            times_today = [9, 14, 21]
        else:
            times_today = [9]

    today = datetime.now().replace(minute=0, second=0, microsecond=0)

    for day_offset in range(duration):
        dose_date = today + timedelta(days=day_offset)
        for hour in times_today:
            scheduled_time = dose_date.replace(hour=hour)
            dose_log = DoseLog(
                prescription_item_id=prescription_item.id,
                scheduled_time=scheduled_time,
                status="pending"
            )
            db.session.add(dose_log)

    db.session.commit()


@app.route('/dashboard')
def dashboard():
    upcoming_doses = DoseLog.query.filter_by(status='pending').order_by(DoseLog.scheduled_time).all()

    dose_list = []
    for dose in upcoming_doses:
        prescription_item = dose.prescription_item
        medicine = prescription_item.medicine
        dose_list.append({
            "id": dose.id,
            "medicine_name": medicine.name,
            "scheduled_time": dose.scheduled_time,
            "food_timing": prescription_item.dosage
        })

    return render_template('dashboard.html', doses=dose_list)


@app.route('/mark_taken/<int:dose_id>')
def mark_taken(dose_id):
    dose = db.session.get(DoseLog, dose_id)
    if dose:
        dose.status = 'taken'
        db.session.commit()
    return redirect('/dashboard')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)