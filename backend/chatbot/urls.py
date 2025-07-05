from django.urls import path
from . import views

urlpatterns = [
    path("api/chat/", views.chat, name="chat"),
    path("api/upload", views.upload_file, name="upload_file"), 
    path("api/pdf", views.ask_pdf, name="ask_pdf"),
]