from django.urls import path
from . import views

urlpatterns = [
    path("api/upload/", views.upload_file_and_ask, name="upload_file_and_ask"),
    path("", views.home, name="home"),
]
