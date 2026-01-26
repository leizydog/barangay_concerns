
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def configure_genai():
    """Configures the Gemini API client."""
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set.")
        return False
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return True

SYSTEM_PROMPT = """
You are "Barangay Bot", a helpful AI assistant for the Barangay Concerns Platform.
Your goal is to assist residents and LGU officials with community issues.

Capabilities:
1. Explain how to file a report (click "Report Concern", fill details).
2. Explain the status workflow (Pending -> In Progress -> Resolved).
3. Provide general advice on safety (e.g., what to do during floods).
4. Be polite, professional, and empathetic.
5. Answer in English or Tagalog/Filipino as requested.

Limitations:
- You CANNOT directly access the database or check specific report status (yet).
- You CANNOT take official reports directly (guide them to the form).
- If asked about specific laws, advise consulting the barangay office.

Tone: Friendly, community-focused, and respectful.
"""

def generate_chat_response(message):
    """Generates a response from Gemini."""
    if not configure_genai():
        return "I'm sorry, my connection to the AI service is currently unavailable. Please contact the administrator."

    try:
        # gemini-flash-latest is the safest alias for the current library version/quota
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Construct prompt with system context
        # Note: Gemini Pro doesn't separate system prompt strongly yet, so we prepend it.
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message}\nAssistant:"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        return "I apologize, but I'm having trouble thinking right now. Please try again later."
