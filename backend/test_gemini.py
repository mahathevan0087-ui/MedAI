# -*- coding: utf-8 -*-
"""
Gemini API Diagnostic Script
Validates API key formats (supporting legacy AIzaSy and new AQ. prefixes),
tests connections via direct HTTP request and the official google-genai SDK.

Usage:
    cd backend
    venv\\Scripts\\python test_gemini.py
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# ──────────────────────────────────────────────
# 1. Load .env
# ──────────────────────────────────────────────
env_path = Path(__file__).resolve().parent / ".env"
print("=" * 60)
print("  MEDAI — GEMINI API DIAGNOSTIC (google-genai)")
print("=" * 60)
print()
print(f"[1] .env path : {env_path}")
print(f"    .env exists: {env_path.exists()}")

if not env_path.exists():
    print("\n  ERROR: .env file not found!")
    print("  Create backend/.env with:  GEMINI_API_KEY=your_key")
    sys.exit(1)

load_dotenv(dotenv_path=env_path, override=True)
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# ──────────────────────────────────────────────
# 2. Inspect the API key
# ──────────────────────────────────────────────
print()
print("[2] API Key check:")

if not API_KEY:
    print("  ERROR: GEMINI_API_KEY is empty or missing from .env")
    sys.exit(1)

prefix = API_KEY[:12]
print(f"  Key prefix  : {prefix}...")
print(f"  Key length  : {len(API_KEY)} characters")

# Accept both legacy 'AIzaSy' and new 'AQ.' formats
if API_KEY.startswith("AIzaSy"):
    print("  Key format  : Legacy/Standard API Key (starts with AIzaSy) - OK")
elif API_KEY.startswith("AQ."):
    print("  Key format  : New Authentication Key (starts with AQ.) - OK")
else:
    print("  Key format  : WARNING: Key starts with unrecognized prefix.")
    print("                Keys typically start with 'AIzaSy' or 'AQ.'.")

# ──────────────────────────────────────────────
# 3. Test HTTP API connectivity directly
# ──────────────────────────────────────────────
print()
print("[3] Testing Direct HTTP REST API connectivity...")
print()

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
payload = {
    "contents": [{"parts": [{"text": "Reply with exactly one word: Hello"}]}],
    "generationConfig": {"maxOutputTokens": 10, "temperature": 0},
}

http_success = False
try:
    resp = requests.post(
        url,
        params={"key": API_KEY},
        json=payload,
        timeout=15,
        headers={"Content-Type": "application/json"},
    )
    print(f"    Direct HTTP Status: HTTP {resp.status_code}")
    if resp.ok:
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        print(f"    Direct HTTP Response: '{text}'")
        http_success = True
    else:
        try:
            err = resp.json()
            code = err.get("error", {}).get("code", "?")
            msg = err.get("error", {}).get("message", resp.text[:200])
            status = err.get("error", {}).get("status", "")
        except Exception:
            code = resp.status_code
            msg = resp.text[:200]
            status = ""
        print(f"    Direct HTTP ERROR: [{code}] {status} — {msg}")
except Exception as e:
    print(f"    Direct HTTP Exception: {e}")

# ──────────────────────────────────────────────
# 4. Test Connectivity via official google-genai SDK
# ──────────────────────────────────────────────
print()
print("[4] Testing Connection via official google-genai SDK...")
print()

sdk_success = False
try:
    from google import genai
    from google.genai.errors import APIError
    
    print("    Initialising Client...")
    client = genai.Client(api_key=API_KEY)
    
    print("    Sending generate_content call...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply with exactly one word: Hello"
    )
    print(f"    SDK Response: '{response.text.strip()}'")
    sdk_success = True
except ImportError:
    print("    SDK ERROR: google-genai package is not installed in this environment.")
except APIError as e:
    print(f"    SDK APIError (HTTP {e.code}): {e.message}")
except Exception as e:
    print(f"    SDK Exception: {e}")

print()

# ──────────────────────────────────────────────
# 5. Diagnostic Summary
# ──────────────────────────────────────────────
print("=" * 60)
if http_success and sdk_success:
    print("  RESULT: SUCCESS")
    print("  Both direct REST and google-genai SDK calls are working perfectly.")
elif sdk_success:
    print("  RESULT: PARTIAL SUCCESS")
    print("  The SDK works, but direct HTTP REST calls are failing.")
elif http_success:
    print("  RESULT: PARTIAL SUCCESS")
    print("  Direct HTTP REST calls work, but the SDK calls are failing.")
else:
    print("  RESULT: FAILED")
    print("\n  POSSIBLE CAUSES & SOLUTIONS:")
    if API_KEY.startswith("AQ."):
        print("  - Your key starts with 'AQ.' and Google API Gateway returned 401.")
        print("    This occurs when the API key's Google Cloud project has the")
        print("    'Generative Language API' disabled, or restrictions are misconfigured.")
        print("    Go to https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
        print("    and ensure the API is ENABLED for your project.")
    print("  - If your project has billing enabled but the free-tier limit is set to 0.")
    print("  - Verify your API key at https://aistudio.google.com/apikey")
print("=" * 60)
sys.exit(0 if (http_success or sdk_success) else 1)
