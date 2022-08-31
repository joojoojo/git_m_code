from django.contrib import admin
from django.urls import path
from .views import UploadSet, Main, Add, Medicine

urlpatterns = [
    path('upload', UploadSet.as_view()),
    path('main', Main.as_view()),
    path('add', Add.as_view()),
    path('medicine', Medicine.as_view()),
    ]