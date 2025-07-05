# backend/chatbot/urls.py
from django.urls import path
from .views import ask_question, index
from django.views.generic import TemplateView

urlpatterns = [
    # CRITICAL CHANGE: This path should be an empty string.
    # When included from the project's urls.py with `path('ask/', include('chatbot.urls'))`,
    # this empty string path will correctly resolve to `/ask/`.
    path("", ask_question, name="ask"),
    path('', index),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/chat/', views.chat, name='chat'),

]