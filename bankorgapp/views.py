from django.shortcuts import render,redirect
from .forms import  AccountCreationForm,LoginForm,TransactionForm
from django.views.generic import CreateView,TemplateView
from .models import MyUser,Transaction
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login,logout
import logging
from django.utils import timezone
from django.contrib import messages
from django.db.models import Value, CharField
from . decorators import loginrequired
from . filters import TransactionFilter
from .forms import FilterForm
from django.db.models import Q
from django.db.models import Case, When, Value, CharField

# Create your views here.

class AccountCreateView(CreateView):
    model=MyUser
    form_class=AccountCreationForm
    template_name='createaccount.html'
    success_url=reverse_lazy('login')



class SigninView(FormView):
    template_name = 'loginpage.html'
    form_class = LoginForm
    success_url = reverse_lazy('home') 

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request, user)  # ✅ THIS logs the user in!
                print("Login success")
                return redirect(self.get_success_url())
            else:
                print('Login Failed')
                form.add_error(None, "Invalid username or password.")
        return render(request, self.template_name, {'form':form})

@loginrequired
def logoutview(request):
    logout(request)
    return redirect('login')

@loginrequired
def balance_view(request):
    balance = request.user.balance
    print(balance)
    return render(request, "home.html", {'balance': balance})
    
logger = logging.getLogger(__name__)
class GetUserAccountMixin():
    def get_user_account(self,acc_no):
        try:
            return MyUser.objects.get(account_number=acc_no)
        except MyUser.DoesNotExist:
            logger.warning(f"Account with number {acc_no} not found.")
            return None
@loginrequired       
def fund_transfer_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            from_account_no = form.cleaned_data['from_account_no']
            to_account_no = form.cleaned_data['to_account_no']
            amount = form.cleaned_data['amount']
            note = form.cleaned_data['note']

            # Ensure sender exists and has sufficient balance
            try:
                sender = MyUser.objects.get(account_number=from_account_no)
                receiver = MyUser.objects.get(account_number=to_account_no)
            except MyUser.DoesNotExist:
                messages.error(request, "Invalid account number.")
                return render(request, "fundtransfer.html", {'form': form})

            if sender.balance < amount:
                messages.error(request, "Insufficient balance.")
                return render(request, "fundtransfer.html", {'form': form})

            # Create transaction
            Transaction.objects.create(
                from_account_no=from_account_no,
                to_account_no=to_account_no,
                amount=amount,
                note=note,
                user=request.user,
                date=timezone.now().date()
            )

            # Update balances
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()

            messages.success(request, "Transaction successful!")
            return redirect('home')
    else:
        form = TransactionForm(user=request.user)

    return render(request, "fundtransfer.html", {'form': form,'user': request.user,'balance': request.user.balance })


@loginrequired
def transaction_history(request):
    user_account_no = request.user.account_number

    Debit_transactions = Transaction.objects.filter(from_account_no=user_account_no).annotate(
        transaction_type=Value('debit', output_field=CharField())
    )
    Credit_transactions = Transaction.objects.filter(to_account_no=user_account_no).annotate(
        transaction_type=Value('credit', output_field=CharField())
    )

    transactions = Debit_transactions.union(Credit_transactions).order_by('-date')

    return render(request, 'transaction_history.html', {
        'transactions': transactions,
        'account_no': user_account_no
    })

# class TransactionFilterView(TemplateView):
#     def get(self,request,*args,**kwargs):
#         transactions=Transaction.objects.filter(Q(to_account_no=request.user.account_number)|Q(from_account_no=request.user.account_number))
       
#         transaction_filter=TransactionFilter(request.GET,queryset=transactions)
#         return render(request,"filterhistory.html",{'filter':transaction_filter})

@loginrequired
def transaction_filter_view(request):
    # Get all transactions related to the user
    account_no = request.user.account_number
    form = FilterForm(request.GET or None)

    transactions = Transaction.objects.none()  # default: show no data

    # transactions = Transaction.objects.filter(
    #     Q(to_account_no=account_no) |
    #     Q(from_account_no=account_no)
    # ).annotate(
    #     transaction_type=Case(
    #         When(from_account_no=account_no, then=Value('debit')),
    #         When(to_account_no=account_no, then=Value('credit')),
    #         output_field=CharField()
    #     )
    # )

    if form.is_valid():
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        amount = form.cleaned_data.get('amount')
        from_account_no = form.cleaned_data.get('from_account_no')
        transaction_type = form.cleaned_data.get('transaction_type')

        # Only run query if at least one filter is applied
        if from_date or to_date or amount or from_account_no or transaction_type:
            transactions = Transaction.objects.filter(
                Q(to_account_no=account_no) |
                Q(from_account_no=account_no)
            ).annotate(
                transaction_type=Case(
                    When(from_account_no=account_no, then=Value('debit')),
                    When(to_account_no=account_no, then=Value('credit')),
                    output_field=CharField()
                )
            )

        if from_date:
            transactions = transactions.filter(date__gte=from_date)
        if to_date:
            transactions = transactions.filter(date__lte=to_date)
        if form.cleaned_data['amount']:
            transactions = transactions.filter(amount=form.cleaned_data['amount'])
        if form.cleaned_data['from_account_no']:
            transactions = transactions.filter(from_account_no=form.cleaned_data['from_account_no'])
        if form.cleaned_data.get('transaction_type'):
            transactions = transactions.filter(transaction_type=form.cleaned_data['transaction_type'])

    transactions = transactions.order_by('-date')

    # Render the filtered result to the template
    return render(request, "filterhistory.html",{
        'transactions': transactions,
        'form': form
        })

    


