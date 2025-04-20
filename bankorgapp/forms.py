from django import forms
from django.contrib.auth.forms import UserCreationForm
from bankorgapp.models import MyUser

class AccountCreationForm(UserCreationForm):
    class Meta:
        model=MyUser
        fields=['first_name','username','email','password1','password2','account_number','account_type',
                'balance','phone_number','address','date_of_birth']
  
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control p-2"}),
            'last_name': forms.TextInput(attrs={"class": "form-control p-2"}),
            'email': forms.TextInput(attrs={"class": "form-control p-2"}),  # ✅ fixed: quotes + casing
            'password1': forms.PasswordInput(attrs={"class": "form-control p-2"}),  # ✅ fixed: wrapped in PasswordInput
            'password2': forms.PasswordInput(attrs={"class": "form-control p-2"}),  # ✅ ditto
            'account_number': forms.TextInput(attrs={"class": "form-control p-2"}),
            'account_type': forms.Select(attrs={"class": "form-control p-2"}),  # ✅ use Select widget for choices
            'balance': forms.NumberInput(attrs={"class": "form-control p-2"}),  # ✅ more appropriate than TextInput
            'phone_number': forms.TextInput(attrs={"class": "form-control p-2"}),
            'address': forms.Textarea(attrs={"class": "form-control p-2", "rows": 3}),
            'date_of_birth': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

class LoginForm(forms.Form):
            username=forms.CharField()
            password=forms.CharField(widget=forms.PasswordInput)
            

            

        