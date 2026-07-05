import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ocr.reader import extract_text
from ai.gemini import analyze_report, ping, API_KEY
import os

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        }
    },
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".pdf"}


def _allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return jsonify({"status": "success", "message": "MedAI backend is running"})


@app.route("/health")
def health():
    """Health-check endpoint — tests Gemini connectivity and shows key prefix."""
    key_prefix = API_KEY[:12] + "..." if len(API_KEY) > 12 else "(too short)"
    key_valid_format = len(API_KEY) > 0

    result = {
        "backend": "ok",
        "api_key_prefix": key_prefix,
        "api_key_format_valid": key_valid_format,
    }

    gemini_result = ping()
    result["gemini"] = "ok" if gemini_result["ok"] else "error"
    if gemini_result["ok"]:
        result["gemini_response"] = gemini_result["response"]
    else:
        result["gemini_error"] = gemini_result["error"]

    status_code = 200 if gemini_result["ok"] else 502
    return jsonify(result), status_code


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not _allowed_file(file.filename):
        return jsonify({
            "error": "Unsupported file type. Please upload a PDF, JPG, PNG, BMP, or TIFF."
        }), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    print(f"✅ File saved: {filepath}")

    try:
        print("⏳ Starting OCR...")
        extracted_text = extract_text(filepath)
        print(f"✅ OCR completed — {len(extracted_text)} characters extracted")

        if not extracted_text.strip():
            return jsonify({
                "status": "error",
                "filename": filename,
                "message": "Could not extract any text from the file. "
                           "Ensure the file is a readable image or PDF.",
            }), 422

        print("⏳ Starting Gemini analysis...")
        analysis = analyze_report(extracted_text)
        print("✅ Gemini analysis completed")

        return jsonify({
            "status": "success",
            "filename": filename,
            "ocr_text": extracted_text,
            "analysis": {
                "summary": analysis.get("summary", ""),
                "abnormal_values": analysis.get("abnormal_values", []),
                "possible_conditions": analysis.get("possible_conditions", []),
                "recommendations": analysis.get("recommendations", []),
            },
        })

    except ValueError as e:
        print(f"❌ ValueError: {e}")
        return jsonify({
            "status": "error",
            "filename": filename,
            "message": str(e),
        }), 422

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return jsonify({
            "status": "error",
            "filename": filename,
            "message": "An unexpected error occurred during processing.",
            "error": str(e),
        }), 500


if __name__ == "__main__":
    # use_reloader=False prevents EasyOCR from loading twice in debug mode
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)