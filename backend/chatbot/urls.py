from django.urls import path
from . import views

urlpatterns = [
    path("api/chat", views.chat, name="chat"),
    path("", views.index, name="index"),
]