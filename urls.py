from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf.urls import url
from . import views as vw

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name = 'loginuser.html'),name ="login"),
    path('home/',vw.index,name = "index"),
    path('addemp/',vw.addemp,name = "addemp"),
    path('addprod/',vw.addproduct,name = "addProduct"),
    path('addtrans/',vw.addtransaction,name ="addtransaction"),
    path('reporting/',vw.reporting,name = "reporting")
]