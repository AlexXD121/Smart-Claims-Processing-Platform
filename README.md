
# Smart Claims Processing Platform

A full-stack AI-powered insurance claims processing platform designed to streamline and automate document analysis, risk assessment, and decision-making using OCR and machine learning.

---

## Features

- Upload scanned or PDF-based insurance claim documents
- Extract text using OCR (Tesseract + PyMuPDF)
- Perform automated risk assessment using ML models
- FastAPI backend with complete CORS support
- Responsive frontend built with React and Vite
- Clean modular architecture (frontend/backend separation)

---

## Project Structure

```
claimpilot/
├── client/                 # Frontend (React/Vite)
├── server/                 # Backend (FastAPI)
│   ├── main.py             # FastAPI entry point
│   ├── utils/              # OCR and ML logic
│   ├── models/             # Pydantic data models
│   └── requirements.txt    # Python dependencies
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AlexXD121/Smart-Claims-Processing-Platform.git
cd Smart-Claims-Processing-Platform
```

### 2. Backend Setup (FastAPI)

```bash
cd server
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

**Note:** Make sure you have Tesseract installed and added to your system's PATH.

Download Tesseract OCR: https://github.com/tesseract-ocr/tesseract

### 3. Frontend Setup (React + Vite)

```bash
cd ../client
npm install
npm run dev
```

---

## Example Use Cases

1. **Upload a Claim Document**  
   Upload a scanned PDF or image file of an insurance claim document.

2. **Text Extraction via OCR**  
   The platform extracts structured text data using Tesseract and PyMuPDF.

3. **Risk Assessment**  
   Automatically evaluates risk using pre-trained machine learning models or rules.

4. **Real-Time Feedback**  
   Displays claim status and insights instantly on the user dashboard.

---

## Technologies Used

**Backend:** Python, FastAPI, PyMuPDF, Tesseract OCR  
**Frontend:** React.js, Vite, Tailwind CSS  
**Other Tools:** Git, GitHub, Postman

---

## Contribution

Contributions are encouraged. Feel free to open an issue or submit a pull request to improve functionality or fix bugs.

Demo Link: https://drive.google.com/file/d/1wgilfIV6H7HUmVpCaZFm6tAbIporfBY-/view?usp=drive_link

---

## License

This project is licensed under the MIT License.
