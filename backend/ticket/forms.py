from django import forms
from django.forms import widgets
from django.forms.widgets import TextInput

PRODUCT_ISSUES = [
    ('Billing Queries', 'Billing Queries'),
    ('Product Issues', 'Product Issues'),
    ('Close Account', 'Close Account'),
]


PRIORITY = [
    ('Normal','Normal'),
    ('Critical', 'Critical'),
    ('High', 'High'),
    ('Low','Low')
]

class WizardTicketInformationsForm(forms.Form):

    selection = forms.CharField(
        label='Submit a Ticket',
        widget=forms.Select(
            attrs={
            'placeholder': 'Submit a ticket',
            'class':'form-control'
            },
            choices=PRODUCT_ISSUES),
            required=True
        )

    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Summary of the problem',
                'class':'form-control'
                }
        ), 
        max_length=100,
        required=True
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control'
                }
        ), 
        max_length=100,
        required=True
    )

    priority = forms.CharField(

        label='Priority',
        widget=forms.Select(
            attrs={
            'placeholder': 'Priority',
            'class':'form-control'
            },
            choices=PRIORITY),
            required=True
        )
    
    due_on = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
                }
        ), 
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        initial='Email Account',
        widget=forms.EmailInput(
            attrs={
                'class':'form-control'
            }
        )
    )


    
