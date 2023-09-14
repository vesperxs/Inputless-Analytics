from re import TEMPLATE
from typing import Any
import json
import stripe
import djstripe
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import View, FormView
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
import os
import subprocess
from django_tenants.utils import schema_context
# Create your views here.
from formtools.wizard.views import SessionWizardView, WizardView
from .forms import WizardSelectPlanForm, WizardInformationForm, WizardAccountForm, WizardConfirmation
from .utils import create_tenant, create_user
from django.core.mail import send_mail, BadHeaderError
from djstripe.models import Product, Customer
from django.contrib.auth.decorators import login_required
from customers.models import Client



FORMS = [
    ("choice", WizardSelectPlanForm),
    ("organization", WizardInformationForm),
    ("register", WizardAccountForm),
    ("confirm", WizardConfirmation)
]

TEMPLATES = {
    "choice": "formtools/wizard/wizard_price_page.html",
    "organization": "formtools/wizard/wizard_organization_form.html",
    "register":"formtools/wizard/wizard_account_form.html",
    "confirm":"formtools/wizard/wizard_confirmation.html"
}

class RegistrationWizard(SessionWizardView):
    #form_list = [WizardInformationForm, WizardAccountForm, WizardCreditCardForm]
    
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def done(self, form_list,**kwargs):
        # max number of tenant daily
        all_data_cleaned = self.get_all_cleaned_data()
        #print(all_data_cleaned)
        tenant = create_tenant(all_data_cleaned)
        create_user(tenant,all_data_cleaned)

        #sync djstripe db to the newly created tenant

        command = "./manage.py tenant_command djstripe_sync_plans_from_stripe --schema={}".format(
            all_data_cleaned['organization'].split('.')[0])
        process = subprocess.Popen(command,shell=True)

        try:
            #'subject', 'message', 'from_email', and 'recipient_list'
            send_mail(
                'Registation',
                'Account {0} created!'.format(all_data_cleaned['organization']),
                all_data_cleaned['email'],
                ['support@vespertiliosrl.com']
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found!')

        #render the link user going to log-in
        return render(self.request,
                      'thanks.html',
                      {"link": all_data_cleaned['organization']
                    })

