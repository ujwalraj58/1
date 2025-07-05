from django.http import JsonResponse
import json
import os
from .langchain_rag import get_answer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "test_chat.html")

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get("message", "")
        return JsonResponse({'response': f"You said: {message}"})
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def ask_question(request):
    # --- TEMPORARY DEBUG PRINT ---
    print("✅ ask_question view was hit!")
    # --- END TEMPORARY DEBUG PRINT ---

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            if not question:
                return JsonResponse({'error': 'No question provided'}, status=400)

            print("🟡 Incoming question:", question)
            answer_object = get_answer(question)

            if hasattr(answer_object, 'content'):
                answer_text = answer_object.content
            else:
                # Fallback in case the structure changes or is unexpected
                answer_text = str(answer_object)

            print("🟢 Got answer:", answer_text)
            return JsonResponse({'answer': answer_text})

        except json.JSONDecodeError:
            print("🔴 JSONDecodeError: Invalid JSON in request body.")
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            print("🔴 Exception occurred:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
