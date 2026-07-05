import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("Key prefix:", API_KEY[:6])

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

r = requests.get(url)

print(r.status_code)
print(r.text)