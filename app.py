from flask import Flask, render_template, request
from models import db
import os
import pytesseract
from PIL import Image

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

    return f"""
    <h2>File uploaded successfully!</h2>
    <p><b>Filename:</b> {file.filename}</p>
    <h3>Extracted Text:</h3>
    <pre>{extracted_text}</pre>
    """

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)