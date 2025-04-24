#from .decorators import user_is_authenticated
from django.contrib import messages
from functools import wraps  
from django.shortcuts import render,redirect
def loginrequired(func):
    @wraps(func)  # ✅ This preserves the function’s name and docstring
    def wrapper(request,*args,**kwargs): #inner function
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('login')
        else:
            return func(request,*args,**kwargs)
    return wrapper
