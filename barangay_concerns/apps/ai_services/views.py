
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .chatbot import generate_chat_response

@require_POST
def chat_api(request):
    """API endpoint for chatbot interactions."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
            
        response_text = generate_chat_response(user_message)
        return JsonResponse({'response': response_text})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
