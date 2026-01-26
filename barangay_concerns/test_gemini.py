
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('GEMINI_API_KEY')
print(f"Key loaded: {key[:5]}...{key[-3:]}")

genai.configure(api_key=key)

try:
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Hello, can you hear me?")
    print("Response:")
    print(response.text)
except Exception as e:
    print("ERROR:")
    print(e)
