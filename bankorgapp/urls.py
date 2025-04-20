from django.urls import path
from .import views
from django.views.generic import TemplateView
from .views import AccountCreateView,SigninView,logoutview,Balanceview
urlpatterns = [
       
        path('register/', AccountCreateView.as_view(), name='signup'),
        path('',SigninView.as_view(),name='login'),
         path('home/',TemplateView.as_view(template_name='home.html'),name='home'),
         path('logout/',views.logoutview, name='signout'),
         path('balance/',Balanceview.as_view(),name='balance')

]


