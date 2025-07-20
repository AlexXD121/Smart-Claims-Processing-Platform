import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def process_multimodal_data(text, doc):
    """
    Extracts text from images inside a PDF using OCR.
    Returns concatenated OCR text or an informative message.
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        ocr_texts = []

        for page in doc:
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                text = pytesseract.image_to_string(image)
                if text.strip():
                    ocr_texts.append(text.strip())

        if ocr_texts:
            return "\n\n".join(ocr_texts)
        else:
            return "No image-based text found."

    except Exception as e:
        print("❌ Image OCR error:", str(e))
        return "Multimodal processing failed."
