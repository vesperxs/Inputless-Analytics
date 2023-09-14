# sendemail/urls.py
from django.contrib import admin
from django.urls import path


from .views import contactView, successView

urlpatterns = [
    path('feedback', contactView, name='contact_us'),
    path('success', successView, name='success'),
]
