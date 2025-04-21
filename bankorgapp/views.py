from django.shortcuts import render,redirect
from .forms import  AccountCreationForm,LoginForm,TransactionForm
from django.views.generic import CreateView,TemplateView
from .models import MyUser,Transaction
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login,logout
from . views import *
import logging
from django.utils import timezone
from django.contrib import messages


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

def logoutview(request):
    logout(request)
    return redirect('login')

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

def fund_transfer_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            Transaction.objects.create(
                from_account_no=form.cleaned_data['from_account_no'],
                to_account_no=form.cleaned_data['to_account_no'],
                amount=form.cleaned_data['amount'],
                note=form.cleaned_data['note'],
                user=request.user,
                date=timezone.now().date()
            )
            messages.success(request, "Transaction successful!")
            return redirect('home')
    else:
        form = TransactionForm(user=request.user)

    return render(request, "fundtransfer.html", {'form': form,'user':request.user,'balance': request.user.balance})



def transaction_history(request):
    transactions = Transaction.objects.filter(from_account_no=request.user.account_number)
    return render(request, 'transaction_history.html', {'transactions': transactions})
