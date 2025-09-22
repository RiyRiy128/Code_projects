"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

app_name = "loan_app"
urlpatterns = [
  path('/', admin.site.urls),
  path("",views.home,name="home"),
  path("bank_admin/",views.bank_admin,name="bank_admin"),
  path("apply/",views.apply,name="apply"),  
  path("details/",views.details,name="details"),  
  path("verification/",views.verification,name="verification"),  
  path("getresult/",views.getresult,name="getresult"),
  path("getresult_admin/",views.getresult_admin,name="getresult_admin"), 
  path("login/",views.login_page,name="login_page"), 
  path("logout/", views.logout_request, name="logout_request"),
  path("terms/", views.terms, name="terms"),
  path("loan_agreement/", views.loan_agreement, name="loan_agreement"),
  path("loan_tips/", views.loan_tips, name="loan_tips"),
  path("howitworks/", views.howitworks, name="howitworks"),
]