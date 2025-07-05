import json
from django.http import JsonResponse
from .langchain_rag import get_answer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .rag_pdf import answer_from_pdf
from .rag_from_uploaded import get_answer_from_file

def home(request):
    return render(request, "test_chat.html")

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        file_path = default_storage.save(f"uploaded/{uploaded_file.name}", uploaded_file)

        try:
            question = request.POST.get('question', '')
            if not question:
                return JsonResponse({'error': 'No question provided'}, status=400)

            answer = get_answer_from_file(file_path, question)
            return JsonResponse({'answer': answer})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def ask_pdf(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get("question", "")
        try:
            response = answer_from_pdf(question)
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get("message", "").strip()

            if not question:
                return JsonResponse({"error": "No message provided"}, status=400)

            answer_obj = get_answer(question)

            # Handle LangChain output
            answer_text = answer_obj.content if hasattr(answer_obj, "content") else str(answer_obj)

            return JsonResponse({"response": answer_text})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

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
