# sendemail/forms.py
from django import forms
from typing import Dict, Any

from django.forms.utils import from_current_timezone


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self) -> Dict[str, Any]:
        super(ContactForm, self).clean()
        email      = self.cleaned_data.get('email','')
        subject    = self.cleaned_data.get('subject','')
        message    = self.cleaned_data.get('message', '')
    
        return self.cleaned_data

class InvitationForm(forms.Form):
    
    email = forms.EmailField(required=True)
    
    def clean(self) -> Dict[str, Any]:
        super(InvitationForm, self).clean()
        email      = self.cleaned_data.get('email','')
        print(email)

        return self.cleaned_data
        
        





