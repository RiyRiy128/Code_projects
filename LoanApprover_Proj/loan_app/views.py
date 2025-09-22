from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from .decisionTables import *
from .forms import loginForm, registerForm
from django.contrib.auth import authenticate, login, get_user_model,logout
from .models import *
# Create your views here
import random
import string
import sys
import datetime

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def apply(request):
  context={}
  return render(request, "apply.html",context);

def home(request):
  context={}
  return render(request, "home.html",context);

def bank_admin(request):
  context={}
  return render(request, "home_admin.html",context);


def details(request):
  context={}
  request.session["amount"]=request.POST['amount']
  request.session["term"]=request.POST['term']
  return render(request, "details.html",context);

def verification(request):
  request.session["age"]=request.POST['age']
  request.session["income"]=request.POST['income']
  request.session["properties"]=request.POST['properties']
  request.session["loans"]=request.POST['loans']
  request.session["credit"]=request.POST['credit']
  
  if 'job' in request.POST:
    #do somethings
    request.session["job"]=1
    print(True)
  else:
    print(False) 
    request.session["job"]=0
  context={}

  return render(request, "verification.html",context);


def getresult_admin(request):
  #machine learning results here.
  #----------------------------------------------
  #maximum amount can loan without taking into account credit score etc.
  reference_code=request.POST['reference']
  context={}
  if(Decision.objects.filter(refnum=reference_code).count()==0):
    return redirect("/bank_admin");
  else:
    decision_attached=Decision.objects.filter(refnum=reference_code)[0]
    print(decision_attached)
    customer_profile=CustomerProfile.objects.filter(user=decision_attached.user)[0]
    print(customer_profile)
    context["id"]=customer_profile.national_id;
    context["amount"]=decision_attached.amount
    context["decision"]=decision_attached.decision
    context["refnum"]=decision_attached.refnum
    context["user"] =decision_attached.user
    context["term_months"]=decision_attached.term_months
    context["first_name"]=decision_attached.user.first_name
    context["last_name"]=decision_attached.user.last_name


  maxEstd=predMaxamount( customer_profile.age, customer_profile.num_unsecured_l_term_all, customer_profile.num_loan_payments_missed, customer_profile.income, customer_profile.num_debit_orders_bounced)
  ###input is only 
  #whether customer defaults or not
  defaultFlag=predDefaultFlag( int(customer_profile.wknd_shopper_flag), int(customer_profile.salary_indicator), customer_profile.num_credit_transactions, customer_profile.house_credit_score, customer_profile.num_properties_owned)###input is 
  #final amount they can loan
  dAmount=decisionTable(customer_profile.age, customer_profile.income, customer_profile.house_credit_score, maxEstd, defaultFlag)
  print(dAmount)
  interest=6
  loandecision=None
  if(decision_attached.term_months>12):
    loandecision=lloanapprover(decision_attached.amount, decision_attached.term_months, customer_profile.income,defaultFlag)
    interest=12
  else:
    loandecision=sloanapprover(decision_attached.amount,dAmount)

  context["admin_suggestion"]=loandecision
  context["interest"]=interest
  total_interest=interestPM(decision_attached.amount,decision_attached.term_months,interest)*decision_attached.term_months
  context["monthly_repayment"]=monthlyrepayment(decision_attached.amount,total_interest,decision_attached.term_months,0)
  
  request.session["amount"]=decision_attached.amount
  request.session["full_name"]=decision_attached.user.first_name+" "+decision_attached.user.last_name
  
  return render(request, "getresult_admin.html",context);







def howitworks(request):
    context={}
    return render(request,"howitworks.html",context);

def terms(request):
    context={}
    return render(request,"terms.html",context);

def loan_agreement(request):
    context={}
    context["amount"]=request.session["amount"]
    context["full_name"]=request.session["full_name"]
    context["datetime"]=datetime.date.today().strftime("%B %d, %Y");
    return render(request,"loan_agreement.html",context);

def loan_tips(request):
    context={}
    return render(request,"loan_tips.html",context);

def getresult(request):
  #machine learning results here.
  #----------------------------------------------
  #maximum amount can loan without taking into account credit score etc.
  maxEstd=predMaxamount(int(request.session["age"]),int(request.session["loans"]),2,int(request.session["income"]),2)
  ###input is only 
  #whether customer defaults or not
  defaultFlag=predDefaultFlag(1,int(request.session["job"]),2,int(request.session["credit"]),int(request.session["properties"]))###input is 
  #final amount they can loan
  dAmount=decisionTable(int(request.session["age"]),int(request.session["income"]),int(request.session["credit"]),maxEstd,defaultFlag)

 
  loandecision=None
  if(int(request.session["term"])>12):
    loandecision=lloanapprover(int(request.session["amount"]),int(request.session["term"]),int(request.session["income"]),defaultFlag)
  else:
    loandecision=sloanapprover(int(request.session["amount"]),dAmount)
    
  print("max loan")
  print(maxEstd)
  print("will likely default?")
  print(defaultFlag)
  print("amount can loan given more vars")
  print(dAmount)
  print("loan  decision")
  print(loandecision);

#-------------------------------------------------------
  context={}
  context["amount"]=request.session["amount"]
  print(context["amount"])
  context["term"]=request.session["term"]
  print(context["term"]);
  context["age"]=request.session["age"]
  print(context["age"]);
  context["income"]=request.session["income"]
  print(context["income"]);
  context["properties"]=request.session["properties"]
  print(context["properties"]);
  context["loans"]=request.session["loans"]
  print(context["loans"]);
  context["credit"]=request.session["credit"]
  print(context["credit"]);
  context["job"]=request.session["job"]
  print(context["job"]);
  context["decision"]=loandecision
  print(context["decision"]);

  reference_code=get_random_string(13)

  context["ref_code"]=reference_code

  mydecision=Decision(user=request.user,decision=loandecision,refnum=reference_code,amount=request.session["amount"],term_months=request.session["term"])
  mydecision.save()
  print(mydecision);
  
  return render(request, "qualification.html",context);

  
def login_page(request):
    form = loginForm(request.POST or None)

    context = {
        "form" : form
    }

    print("user logged in")
    

    
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username = username, password = password)
        print(request.user.is_authenticated)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            context['form'] = loginForm()
            context["error"]=None
            return redirect("/")
        else:    
            # return invalid login
            context["error"]="Incorrect Username or Password"
            print("error")
    return render(request, "login.html",context)

def logout_request(request):
    logout(request)
    return redirect("/")
    
    
User = get_user_model()
def register_page(request):
    form = registerForm(request.POST or None)

    context = {
        "form" : form
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        new_user = User.objects.create_user(username,email,password)
        new_user.is_active = True
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        print(new_user)
        return redirect("/login")
    return render(request, "register.html", context)

