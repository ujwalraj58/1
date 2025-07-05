# backend/chatbot/urls.py
from django.urls import path
from .views import ask_question

urlpatterns = [
    # CRITICAL CHANGE: This path should be an empty string.
    # When included from the project's urls.py with `path('ask/', include('chatbot.urls'))`,
    # this empty string path will correctly resolve to `/ask/`.
    path("", ask_question, name="ask"),
]
