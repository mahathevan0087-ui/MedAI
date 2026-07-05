# -*- coding: utf-8 -*-
"""
Gemini AI integration using the official google-genai==2.10.0 SDK.
Implements robust retry with exponential backoff, fallback models,
prompt truncation, and strict 30-second timeout control.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os
import json
import time
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Resolve and load environment variables from backend/.env
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

__all__ = ["analyze_report", "ping", "API_KEY"]

# Fallback chain as requested: best available models
MODEL_FALLBACK_CHAIN = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

MAX_TOTAL_TIMEOUT = 30.0  # Max request time: 30 seconds
MAX_RETRIES = 5  # Up to 5 attempts per model on retryable errors


def _get_client():
    """Initialise and return the Google GenAI client."""
    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set in backend/.env. "
            "Please generate one at https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=API_KEY)


def ping() -> dict:
    """
    Test Gemini connectivity using the primary model.
    Used by /health endpoint.
    """
    try:
        client = _get_client()
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                client.models.generate_content,
                model=MODEL_FALLBACK_CHAIN[0],
                contents="Reply with only OK."
            )
            response = future.result(timeout=10.0)
            
        return {
            "ok": True,
            "response": response.text.strip()
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }


def _call_with_backoff_and_fallback(prompt: str, start_time: float) -> str:
    """
    Executes generate_content across the model fallback chain
    with exponential backoff retries on 503, 429, and 500 errors.
    """
    client = _get_client()
    last_error = None

    for model in MODEL_FALLBACK_CHAIN:
        print(f"[Gemini] Attempting analysis with model: {model}...")
        
        attempt = 0
        backoff_delay = 1.0  # Start with 1.0 second delay
        
        while attempt < MAX_RETRIES:
            # Enforce overall 30s timeout across all attempts
            elapsed = time.time() - start_time
            remaining_timeout = MAX_TOTAL_TIMEOUT - elapsed
            if remaining_timeout <= 1.0:
                raise TimeoutError("Total request time exceeded the 30-second limit.")
                
            try:
                # Call generate_content under a strict remaining timeout limit
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(
                        client.models.generate_content,
                        model=model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.2,
                        )
                    )
                    response = future.result(timeout=remaining_timeout)
                    
                # Validate response structure
                if not response.text:
                    raise ValueError("Empty response returned from the model.")
                    
                print(f"✅ Success with model: {model} on attempt {attempt + 1}")
                return response.text.strip()
                
            except (APIError, Exception) as e:
                attempt += 1
                last_error = e
                status_code = getattr(e, "code", None)
                
                # Identify if this is a retryable error (503, 429, 500)
                is_retryable = False
                if isinstance(e, APIError) and status_code in (429, 500, 503):
                    is_retryable = True
                elif "503" in str(e) or "429" in str(e) or "500" in str(e) or "demand" in str(e).lower():
                    is_retryable = True

                if is_retryable and attempt < MAX_RETRIES:
                    print(f"⚠️ Warning: Model {model} returned retryable error (HTTP {status_code}). "
                          f"Retrying in {backoff_delay}s... (Attempt {attempt}/{MAX_RETRIES})")
                    time.sleep(backoff_delay)
                    backoff_delay *= 2.0  # Exponential backoff doubling
                else:
                    print(f"❌ Model {model} failed on attempt {attempt}: {e}")
                    break  # Stop retrying this model, proceed to the next fallback

    # If all models in the fallback chain fail, raise the final exception
    if last_error:
        raise last_error
    raise ValueError("All Gemini fallback models failed to generate content.")


def analyze_report(report_text: str) -> dict:
    """
    Analyze OCR-extracted medical report text.
    Handles timeout, truncation, rate limiting, and structured JSON normalization.
    """
    start_time = time.time()
    
    # 1. Truncate OCR text safely if too large (limit to ~10,000 characters)
    max_char_limit = 10000
    if len(report_text) > max_char_limit:
        print(f"[Gemini] OCR text too large ({len(report_text)} chars). Truncating safely to {max_char_limit}...")
        report_text = report_text[:max_char_limit] + "\n[Medical Report Text Truncated due to size constraints]"

    # Prepare prompt
    prompt = f"""You are an experienced medical assistant.

Analyze the following medical report.

Return ONLY valid JSON matching this schema:
{{
  "summary": "Brief summary. Warn that a doctor should confirm findings.",
  "abnormal_values": ["value 1 (High/Low)", "value 2"],
  "possible_conditions": ["condition 1", "condition 2"],
  "recommendations": ["action 1", "action 2"]
}}

Rules:
1. Summarize the report.
2. Identify abnormal values.
3. Identify possible diseases (never diagnose with certainty, always suggest confirmation).
4. Recommend next medical actions.

Medical Report:
{report_text.strip()}
"""

    try:
        # Execute query with backoff and fallbacks
        response_text = _call_with_backoff_and_fallback(prompt, start_time)
        
    except TimeoutError as te:
        raise ValueError(str(te))
    except APIError as e:
        status_code = getattr(e, "code", None)
        message = getattr(e, "message", str(e))
        if status_code == 401:
            raise ValueError("Authentication failed: Your API key is invalid or expired.")
        elif status_code == 403:
            raise ValueError("Access Forbidden: Ensure the Generative Language API is enabled for this key.")
        elif status_code == 429:
            raise ValueError("Quota/Rate Limit Exceeded: Please upgrade your billing plan or check API limits.")
        else:
            raise ValueError(f"Gemini API error (HTTP {status_code}): {message}")
    except Exception as e:
        raise ValueError(f"Failed to analyze report: {e}")

    # Clean markdown formatting code blocks if present
    if response_text.startswith("```"):
        lines = response_text.splitlines()
        clean_lines = [l for l in lines if not l.strip().startswith("```")]
        response_text = "\n".join(clean_lines).strip()

    # Extract the JSON bounding braces
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"Failed to parse Gemini response: No valid JSON found:\n{response_text[:300]}")

    json_text = response_text[start:end]

    try:
        analysis = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode response JSON: {e}\nRaw output:\n{response_text[:300]}")

    # Normalize response JSON structure to guarantee schema compatibility
    return {
        "summary": str(analysis.get("summary", "No summary available.")),
        "abnormal_values": _to_str_list(analysis.get("abnormal_values", [])),
        "possible_conditions": _to_str_list(analysis.get("possible_conditions", [])),
        "recommendations": _to_str_list(analysis.get("recommendations", [])),
    }


def _to_str_list(value) -> list:
    """Helper to safely coerce a list of mixed types to a list of strings."""
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        if isinstance(item, dict):
            result.append(", ".join(f"{k}: {v}" for k, v in item.items()))
        else:
            result.append(str(item))
    return result