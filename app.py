from flask import Flask, render_template, request
from models import db, Medicine
import os
import pytesseract
from PIL import Image
from matcher import find_best_match, extract_candidate_words
from parser import parse_dosage_info

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

    # Try matching each line against our medicine list, and parse dosage info
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
            matches_found.append({
                "original": line,
                "matched": best_match,
                "confidence": confidence,
                "frequency": dosage_info["frequency"],
                "food_timing": dosage_info["food_timing"],
                "duration_days": dosage_info["duration_days"]
            })
            seen.add(best_match)

    return render_template('result.html',
                            filename=file.filename,
                            extracted_text=extracted_text,
                            matches=matches_found)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)