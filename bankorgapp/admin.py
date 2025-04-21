from django.contrib import admin
from .models import MyUser,Transaction
#Register your models here.
admin.site.register(MyUser)
admin.site.register(Transaction)