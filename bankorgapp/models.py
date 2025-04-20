from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    # Extend built-in User model if needed

    ACCOUNT_TYPES = (
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
        ('LOAN', 'Loan'),
    )

    account_number = models.CharField(max_length=12, unique=True)
    account_type = models.CharField(max_length=16, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True)

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)  # load default behavior first

    # Then override specific things
    self.fields['phone_number'].required = False
    self.fields['balance'].widget.attrs['readonly'] = True
    
