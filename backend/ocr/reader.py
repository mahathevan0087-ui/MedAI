import os
import fitz  # PyMuPDF — already installed (pymupdf 1.28.0)
import easyocr

# Lazy-initialise EasyOCR so it doesn't load on import
# (avoids double-init caused by Flask's debug reloader)
_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        print("⏳ Initialising EasyOCR (first request only)...")
        _reader = easyocr.Reader(["en"], gpu=False)
        print("✅ EasyOCR ready")
    return _reader


def extract_text(file_path: str) -> str:
    """
    Extract text from an image or PDF file.

    For PDFs:
      1. Try direct text extraction (works for digital/text-layer PDFs).
      2. If empty, fall back to OCR on rendered page images (scanned PDFs).

    For images (JPG, PNG, BMP, TIFF, etc.):
      Run EasyOCR directly.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    else:
        return _extract_from_image(file_path)


def _extract_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF — digital text first, OCR fallback."""
    doc = fitz.open(pdf_path)

    # Attempt 1: direct text layer (fast, accurate for non-scanned PDFs)
    text_parts = []
    for page in doc:
        page_text = page.get_text().strip()
        if page_text:
            text_parts.append(page_text)
    doc.close()

    direct_text = "\n".join(text_parts).strip()
    if direct_text:
        print("✅ PDF text extracted directly (text layer)")
        return direct_text

    # Attempt 2: OCR on rendered page images (scanned / image-only PDFs)
    print("⚠️  No text layer found in PDF — falling back to OCR on page images")
    reader = _get_reader()
    doc = fitz.open(pdf_path)
    ocr_parts = []
    for page_num, page in enumerate(doc):
        print(f"   OCR page {page_num + 1}/{len(doc)}...")
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        results = reader.readtext(img_bytes)
        page_text = "\n".join(r[1] for r in results)
        ocr_parts.append(page_text)
    doc.close()

    return "\n".join(ocr_parts).strip()


def _extract_from_image(image_path: str) -> str:
    """Extract text from an image file using EasyOCR."""
    reader = _get_reader()
    results = reader.readtext(image_path)
    return "\n".join(r[1] for r in results).strip()