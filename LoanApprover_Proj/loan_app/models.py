from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.conf import settings
from django.db.models.manager import Manager
from django.contrib.auth import authenticate

# Create your models here.
#Customer model
User = settings.AUTH_USER_MODEL
class CustomerProfile(models.Model):
    national_id=models.CharField(max_length=13)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    age=models.IntegerField(default=18)
    income=models.IntegerField(default=3000)
    num_unsecured_l_term_all = models.IntegerField(default = 1)
    num_loan_payments_missed = models.IntegerField(default = 0)
    num_debit_orders_bounced = models.IntegerField(default = 3)
    wknd_shopper_flag = models.BooleanField(default=False)
    salary_indicator = models.BooleanField(default=True)
    num_credit_transactions = models.IntegerField(default = 12)
    house_credit_score = models.IntegerField(default = 0)
    num_properties_owned = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.user.first_name

class Decision(models.Model):
    decision=models.BooleanField(default=False)
    refnum=models.CharField(max_length=13)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()
    term_months=models.IntegerField()




