from django import forms
from django.forms import widgets
from django.forms.widgets import TextInput
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



ACCOUNT_TYPE =(
    ("demo", "demo"),
    ("professional", "professional")
   )
  


class WizardSelectPlanForm(forms.Form):
    pass


class WizardInformationForm(forms.Form):

    country = CountryField().formfield(
            widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        )
    )

    tenant_type = forms.ChoiceField(
        label='Account Type',
        choices=ACCOUNT_TYPE,
        widget=forms.Select(
            attrs={
                'placeholder':'Account Type',
                'class':'form-control',
            }
        )
    )

    
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Address Address',
                'class':'form-control'
                }
        ), 
        max_length=100,
        required=True
    )

    cap  = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Cap',
                'class':'form-control'
            }
        ),
        required=True
    )

    province = forms.CharField(

        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter Province',
                'class':'form-control'
            }
        ),
    max_length=100,
    required=True
    )


    city  = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter City',
                'class':'form-control'
            }
        ),
        max_length=100, 
        required=True
    )

    iva  = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter p.iva',
                'class':'form-control'
            }
        ),
        min_value=11
    )




class WizardAccountForm(forms.Form):
    """
    User account informations
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter username',
                'class':'form-control'
            }
        ),
    max_length=150, 
    required=True
    )

    password  = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Enter Password',
                'class':'form-control'
            }
        ),
        max_length=100,
        required=True
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter username',
                'class':'form-control'
            }
        ),
    max_length=150, 
    required=True
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Lastname',
                'class':'form-control'
            }
        ),
    max_length=150, 
    required=True
    )
    
    email = forms.EmailField( 
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter email',
                'class':'form-control'
            }
        ),
        max_length=100,
        required=True
    )

    organization = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter Organization',
                'class':'form-control'
            }
        ),
        
        max_length=100, 
        required=True
    )
    
    phone  = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter phone',
                'class':'form-control'
            }
        ),
    #prefisso
    )






class WizardConfirmation(forms.Form):
    pass





