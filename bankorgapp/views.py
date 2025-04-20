from django.shortcuts import render,redirect
from .forms import  AccountCreationForm,LoginForm
from django.views.generic import CreateView,TemplateView
from .models import MyUser
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login,logout


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

class Balanceview(TemplateView):
    template_name="home.html"
    def get(self,request,*args,**kwargs):
        balance=request.user.balance
        print(balance)
        return render(request, self.template_name,{'balance':balance})
       

