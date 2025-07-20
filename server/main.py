from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import docx2txt
import traceback
from claims_classifier import classify_claim
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_MIME_TYPES = {
    "application/pdf": "pdf",
    "image/jpeg": "image",
    "image/png": "image",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "text/plain": "txt"
}

def extract_from_pdf(file_bytes):
    try:
        doc = fitz.open("pdf", file_bytes)
        full_text = ""
        for page in doc:
            text = page.get_text().strip()
            if not text:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                text = pytesseract.image_to_string(img)
            full_text += text + "\n"
        return full_text.strip()
    except Exception as e:
        return f"[Error in PDF extraction] {str(e)}"

def extract_from_image(file_bytes):
    try:
        img = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"[Error in image OCR] {str(e)}"

def extract_from_docx(file_bytes):
    try:
        with open("temp.docx", "wb") as f:
            f.write(file_bytes)
        text = docx2txt.process("temp.docx")
        return text.strip()
    except Exception as e:
        return f"[Error in DOCX extraction] {str(e)}"

def extract_from_txt(file_bytes):
    try:
        return file_bytes.decode('utf-8').strip()
    except Exception as e:
        return f"[Error in TXT extraction] {str(e)}"

def extract_text(file: UploadFile, content: bytes):
    mime = file.content_type
    if mime not in ALLOWED_MIME_TYPES:
        return "[Unsupported file type]"

    extractor_type = ALLOWED_MIME_TYPES[mime]

    if extractor_type == "pdf":
        return extract_from_pdf(content)
    elif extractor_type == "image":
        return extract_from_image(content)
    elif extractor_type == "docx":
        return extract_from_docx(content)
    elif extractor_type == "txt":
        return extract_from_txt(content)
    else:
        return "[Unsupported extractor]"

@app.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        try:
            start_time = datetime.utcnow().isoformat()
            content = await file.read()
            extracted_text = extract_text(file, content)

            classification = classify_claim(extracted_text)

            result = {
                "filename": file.filename,
                "status": "Processed",
                "text": extracted_text[:1500],
                "timestamp": start_time,
                **classification
            }

            results.append(result)

        except Exception as e:
            traceback.print_exc()
            results.append({
                "filename": file.filename,
                "status": "Failed",
                "error": str(e)
            })

    return {"results": results}
