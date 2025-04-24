# filters.py
import django_filters 
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields=["date","amount","from_account_no"]
        
