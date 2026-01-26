import google.generativeai as genai
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

def get_gemini_model():
    """
    Configure and return the Gemini model.
    """
    if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set.")
        return None
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    return model

def analyze_concern(title, description):
    """
    Analyze a concern report to suggest category and priority.
    """
    model = get_gemini_model()
    if not model:
        return None

    prompt = f"""
    You are an intelligent assistant for a Barangay Concern Reporting System.
    Analyze the following report and suggest the best Category and Priority.
    
    Categories: 
    - FLOOD (Flooding, drainage issues)
    - ROAD (Potholes, broken path, obstruction)
    - WASTE (Garbage, uncollected trash)
    - ELECTRICITY (No power, broken street light)
    - WATER (No water, leak, dirty water)
    - SAFETY (Crime, drugs, fight, suspicious)
    - HEALTH (Dengue, sickness, sanitation)
    - OTHER (Anything else)
    
    Priorities:
    - LOW (Minor issue, no immediate danger)
    - MEDIUM (Needs attention but not critical)
    - HIGH (Significant breakage, health risk, or major inconvenience)
    - URGENT (Immediate danger to life or property, severe flooding/fire/crime)

    Report Title: {title}
    Report Description: {description}
    
    Respond STRICTLY in JSON format:
    {{
        "category": "CATEGORY_CODE", 
        "priority": "PRIORITY_CODE",
        "reasoning": "Short explanation why"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        if "```" in text:
            text = text.replace("```json", "").replace("```", "")
        
        data = json.loads(text.strip())
        return data
    except Exception as e:
        logger.error(f"Error calling Gemini: {e}")
        return None
