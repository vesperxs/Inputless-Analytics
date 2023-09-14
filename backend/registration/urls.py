from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import FORMS

urlpatterns = [
    path('registration/', views.RegistrationWizard.as_view(FORMS), name="registration"),
]
