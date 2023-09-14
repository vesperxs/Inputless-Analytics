# Create your views here.
from django.shortcuts import render
from django.views.generic import View, FormView
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse
# Create your views here.
from formtools.wizard.views import SessionWizardView
from .forms import WizardTicketInformationsForm
from django.core.mail import send_mail, BadHeaderError



FORMS = [("address", WizardTicketInformationsForm)]


TEMPLATES = {"address": "formtools/wizard/wizard_form_ticket.html"}



class CheckoutTicketWizard(SessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list,**kwargs):
        #data_for_step1 = self.get_cleaned_data_for_step('1')

        all_data_cleaned = self.get_all_cleaned_data()
        content = [(k,v) for k,v in all_data_cleaned.items()]

        try:
            #'subject', 'message', 'from_email', and 'recipient_list'
            send_mail('TicketSupport',
                      str(content),
                      all_data_cleaned['email'],
                      ['support@vespertiliosrl.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found!')
            
        #print(data_for_step1)
        
        #get tenant name
        #send email to us

        
        
        return render(self.request, 'thanks_ticket.html') 
