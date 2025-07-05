import json
from django.http import JsonResponse
from .langchain_rag import handle_user_query
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from .rag_pdf import answer_from_pdf
from .rag_from_uploaded import get_answer_from_file
from .langchain_rag import create_vectorstore_from_pdf, handle_user_query

def home(request):
    return render(request, "test_chat.html")

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            retriever = create_vectorstore_from_pdf("chatbot/static/data/AI Chatbot for Student Assistance.pdf")
            body = json.loads(request.body)
            user_input = body.get("message")
            session_id = body.get("session_id", get_random_string(12))

            response = handle_user_query(user_input, retriever, session_id)

            return JsonResponse({"response": response, "session_id": session_id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Send a POST request with 'message'."})

@csrf_exempt
def upload_file_and_ask(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        question = request.POST.get('question')

        if not file or not question:
            return JsonResponse({'error': 'File and question required'}, status=400)

        # Save the uploaded file temporarily
        file_path = os.path.join("temp", file.name)
        with open(file_path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Process the file using your RAG function
        try:
            answer = process_pdf_with_rag(file_path, question)
            return JsonResponse({'answer': answer})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

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

            answer_obj = handle_user_query(question)

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
            answer_object = handle_user_query(question)

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
