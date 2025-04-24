from django import forms
from django.contrib.auth.forms import UserCreationForm
from bankorgapp.models import MyUser,Transaction
from .models import MyUser
import logging

logger = logging.getLogger(__name__)

class GetUserAccountMixin:
    def get_user_account(self, acc_no):
        try:
            return MyUser.objects.get(account_number=acc_no)
        except MyUser.DoesNotExist:
            logger.warning(f"Account with number {acc_no} not found.")
            return None

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
            username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control p-2"}))
            password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control p-2"}))


class FilterForm(forms.Form):
    TRANSACTION_CHOICES = (
        ('', 'All'),
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    from_account_no = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    transaction_type = forms.ChoiceField(
        required=False,
        choices=TRANSACTION_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

           

class TransactionForm(forms.Form,GetUserAccountMixin):
     from_account_no=forms.CharField(max_length=16)
     to_account_no=forms.CharField(max_length=16)
     confirm_account_no=forms.CharField(max_length=16)
     amount=forms.DecimalField()
     note=forms.CharField(max_length=100)

     def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['from_account_no'].initial = self.user.account_number
            self.fields['from_account_no'].widget.attrs['readonly'] = True
     
     
     def clean(self):
          cleaned_data=super().clean()
          from_account_no=self.user.account_number if self.user else None
          to_account_no=cleaned_data.get("to_account_no")
          confirm_account_no=cleaned_data.get("confirm_account_no")
          amount=cleaned_data.get("amount")

          if amount is not None and amount <= 0:
               self.add_error("amount","Amount should be greater than zero.")
               


                      # Check if account numbers match
          if to_account_no != confirm_account_no:
                self.add_error("confirm_account_no", "Account numbers do not match.")

           # Check if the target account exists
          account = self.get_user_account(confirm_account_no)
          if not account:
                self.add_error("confirm_account_no", "Invalid account number.")

             # ✅Check sender's balance
          if self.user and amount:
                 if self.user.balance<amount:
                      self.add_error("amount","Insufficient balance")

          return cleaned_data

          









        


   
    
            

            

        