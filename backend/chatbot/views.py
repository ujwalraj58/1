import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .langchain_rag import get_qa_chain, create_vectorstore_from_pdf

@csrf_exempt
def upload_file_and_ask(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        question = request.POST.get('question')

        if not uploaded_file or not question:
            return JsonResponse({'error': 'File and question required'}, status=400)

        # Save file temporarily
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Process with RAG
        try:
            retriever = create_vectorstore_from_pdf(file_path)
            qa_chain = get_qa_chain(retriever)
            answer = qa_chain.run(question)
            return JsonResponse({'answer': answer})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
