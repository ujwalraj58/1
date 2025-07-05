from django.urls import path
from .views import ask_question, index
from . import views

urlpatterns = [
    path("api/chat", views.ask_question, name="chat"),
    path("", views.index, name="index"),
]