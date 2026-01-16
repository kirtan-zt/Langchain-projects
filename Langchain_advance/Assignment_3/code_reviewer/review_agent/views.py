import os
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.error("WARNING: GROQ_API_KEY is not set in environment variables!")

client = Groq(api_key=api_key)

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {
                        "role": "system", 
                        "content": """
                                    You are a professional code reviewer. 
                                    Provide a summary of code quality, potential bugs,
                                    performance improvement suggestions, security considerations, 
                                    readability suggestions, fix examples.
                                   """
                    },
                    {"role": "user", "content": user_message},
                ],
                max_tokens=2000
            )
            
            ai_message = response.choices[0].message.content
            return JsonResponse({'message': ai_message})
            
        except Exception as e:
            logger.error(f"AI Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'review_agent/index.html')