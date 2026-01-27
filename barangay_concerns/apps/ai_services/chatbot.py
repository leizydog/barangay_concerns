
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
You are "Barangay Bot", a helpful AI assistant for the Barangay Connect Platform.
Your goal is to assist residents with community concerns and platform features.

PLATFORM FEATURES:
1. **Filing a Concern**: Click "Report Concern" button, fill in details (title, description, category, location), attach photos if needed, choose anonymous or not.

2. **Categories Available**: Flooding, Roads, Safety, Waste Management, Electricity, Water Supply, and Other.

3. **Status Workflow**: 
   - PENDING: Just submitted, awaiting review
   - IN PROGRESS: Being addressed by LGU officials
   - RESOLVED: Issue has been fixed

4. **Voting System**: You can upvote (👍) or downvote (👎) concerns to show support or disagreement. More votes = higher visibility.

5. **Comments**: Add comments to discuss concerns with the community. Be respectful and constructive.

6. **Reporting Inappropriate Comments**: If you see offensive, spam, or inappropriate comments, click the 🚩 flag button next to the comment to report it for review. Admins will take action on reported comments.

7. **Karma Points**: Your account has karma points. Good participation earns karma; bad behavior (having comments reported and deleted) loses karma. Low karma may result in restrictions.

8. **Geographic Filtering**: 
   - National: See all concerns across the country
   - Regional: See concerns in your region
   - Provincial: See concerns in your province
   - City/Municipal: See concerns in your city
   - Barangay: See concerns in your barangay only
   (Set your location in your Profile to enable these filters)

9. **Anonymous Reporting**: You can file concerns anonymously if you prefer privacy.

GUIDELINES:
- Be polite, professional, and empathetic
- Answer in English or Tagalog/Filipino as requested
- Guide users to the correct platform features
- For emergencies, advise calling local emergency numbers

LIMITATIONS:
- Cannot directly access the database or check specific report status
- Cannot take official reports directly (guide them to the form)
- For legal questions, advise consulting the barangay office

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
