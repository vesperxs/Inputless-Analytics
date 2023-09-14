from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import FORMS
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    #staff members
	path('ticket', staff_member_required(views.CheckoutTicketWizard.as_view(FORMS))),
]
