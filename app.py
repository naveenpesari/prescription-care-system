from flask import Flask, render_template, request
from models import db, Medicine
import os
import pytesseract
from PIL import Image
from matcher import find_best_match

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

    # Break OCR text into words/lines, clean them up
    words = extracted_text.split('\n')
    words = [w.strip() for w in words if len(w.strip()) > 3]  # ignore very short junk

    # Try matching each line/word against our medicine list
    matches_found = []
    seen = set()

    for word in words:
        best_match, distance, confidence = find_best_match(word, medicine_names)
        if confidence >= 0.6 and best_match not in seen:  # only good matches
            matches_found.append((word, best_match, confidence))
            seen.add(best_match)

    return render_template('result.html',
                            filename=file.filename,
                            extracted_text=extracted_text,
                            matches=matches_found)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)