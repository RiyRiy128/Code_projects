from django import forms
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput
from django.contrib.auth import get_user_model



User = get_user_model()
class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Username',
        'required':'required'
        }
    ))
    password = forms.CharField(widget= forms.PasswordInput( attrs={
        'class':'form-control',
        'placeholder':'Password',
        'required':'required'
        }))

class registerForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Username',
        'required':'required'
        }
    ))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'First name',
        'required':'required'
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
      attrs={
        'class':'form-control',
        'placeholder':'Last name',
        'required':'required'
        }
    ))

    password = forms.CharField(widget = forms.PasswordInput( 
      attrs={
        'class':'form-control',
        'placeholder':'Password',
        'required':'required'
        }
    ))

    conf_password = forms.CharField(label = "Confirm password",widget = forms.PasswordInput( 
      attrs={
        'class':'form-control',
        'placeholder':'Confirm Password',
        'required':'required'
        }
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Email',
        'required':'required',
        'type':'email'
        }
    ))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username= username)
        if qs.exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise forms.ValidationError("email already exists")
        return email    

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('conf_password')

        if password2 != password:
            raise forms.ValidationError("passwords must match")
        return data    


