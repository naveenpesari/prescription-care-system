# 💊 Prescription Care System

An AI-assisted system that reads prescription images, identifies medicines using a custom fuzzy-matching algorithm, extracts dosage instructions, schedules dose reminders, and flags potentially dangerous drug interactions.

## 🩺 The Problem

Millions of people struggle to read messy or handwritten prescriptions, forget doses, or unknowingly take medicine combinations that interact dangerously. This project explores how OCR and classic algorithms can turn a photo of a prescription into a reliable, structured care plan.

## ✨ Features

- **OCR-based text extraction** from prescription images (Tesseract)
- **Custom fuzzy matching algorithm** (Levenshtein Distance, implemented from scratch) to correctly identify medicine names even when OCR output is imperfect
- **Regex-based dosage parser** that extracts frequency, food timing, and duration from unstructured text
- **Automatic dose scheduling** — generates individual reminder entries for every dose across the full treatment course
- **Dose tracking dashboard** — view upcoming doses and mark them as taken
- **Drug interaction checker** — hashmap-based lookup that warns about known dangerous medicine combinations

## 🧠 Core Algorithms & DSA Concepts

| Feature | Concept Used |
|---|---|
| Medicine name matching | Levenshtein Distance (Dynamic Programming) |
| Medicine database lookup | Hashmap (O(1) lookup) |
| Drug interaction checking | Hashmap of medicine pairs |
| Dose scheduling | Time-based iteration and sorting |
| Dosage text parsing | Regex pattern matching |

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via SQLAlchemy ORM)
- **OCR:** Tesseract OCR (pytesseract)
- **Image Processing:** Pillow

## 📸 How It Works

1. User uploads a photo of a prescription
2. Tesseract OCR extracts raw text from the image
3. Each line is compared against a medicine database using a custom Levenshtein Distance algorithm
4. Matched medicines are parsed for frequency, food timing, and duration using regex
5. The system generates a full dose schedule and saves everything to the database
6. Multiple medicines are checked against each other for known dangerous interactions
7. Users can view and track upcoming doses on a dashboard

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/naveenpesari/prescription-care-system.git
cd prescription-care-system

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

**Note:** Requires [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed separately, with the path configured in `app.py`.

## 🔮 What I'd Improve With More Time

- Add regional language support (Kannada/Hindi) for prescriptions
- Confidence-based manual confirmation UI for low-confidence OCR matches
- Caretaker mode with SMS/email alerts for missed doses
- Expand the drug interaction database with a verified medical source
- Add proper multi-user support with authentication

## 👤 Author

Naveen Peesari