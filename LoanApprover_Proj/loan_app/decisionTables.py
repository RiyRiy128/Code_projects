###adjustable decision table for estimated loan amount considering age and credit score###
from joblib import load
import os

dflaglog_dir= os.path.abspath("dFlagLog.joblib")
maxE_dir=os.path.abspath('maxEstimated.joblib')

df_model = load(dflaglog_dir)
maxE_model = load(maxE_dir)
def predDefaultFlag(w,s,c,h,n):###input is only integers###
    pred=[[w,s,c,h,n]]####[[weekendFlag,SalaryIndicator,Total number of credit card transactions over last 12 months,HouseholdCreditScore,NumPropertiesEverOwned]]
    print("The Prediction default flag is: ",df_model.predict(pred))
    return (df_model.predict(pred))

def predMaxamount(a,n,nlr,i,d):###input is only integers###
    pred=[[a,n,nlr,i,d]]####[[age,Number of unsecured long term across all credit providers,Number of loan repayments you have missed over the last 90 days,Income,Number of debit orders that bounced on your cheque account because of insufficient funds]]
    print("The Predicion Max Amount is: ",df_model.predict(pred))
    return(maxE_model.predict(pred))

def decisionTable(age,income,creditScore,maxEstd,defaultFlag):
    ###you can play around with this for different kinds of loans by times by different percentages###
    loan=0
    if(income==0 or maxEstd<=0 or age<18):
        loan=0
        return loan
    elif (age>=18 and age<=35 and defaultFlag==0):
        if(creditScore>600):
            loan=maxEstd
            return loan
        elif(creditScore<=600 and creditScore>=581):
            loan=0.8*maxEstd
            return loan
        elif(creditScore<=580 and creditScore>=1):
            loan=0.4*maxEstd
            return loan
    elif (age>=18 and age<=35 and defaultFlag==1):
        if(creditScore>600):
            loan=0.9*maxEstd
            return loan
        elif(creditScore<=600 and creditScore>=581):
            loan=0.7*maxEstd
            return loan
        elif(creditScore<=580 and creditScore>=1):
            loan=0.3*maxEstd
            return loan
    elif (age>=36 and age<=59 and defaultFlag==0):
        if(creditScore>600):
            loan=1.5*maxEstd
            return loan
        elif(creditScore<=600 and creditScore>=581):
            loan=1.3*maxEstd
            return loan
        elif(creditScore<=580 and creditScore>=1):
            loan=0.5*maxEstd
            return loan
    elif (age>=36 and age<=59 and defaultFlag==1):
        if(creditScore>600):
            loan=0.95*maxEstd
            return loan
        elif(creditScore<=600 and creditScore>=581):
            loan=0.8*maxEstd
            return loan
        elif(creditScore<=580 and creditScore>=1):
            loan=0.5*maxEstd
            return loan
    elif (age>=60 and defaultFlag==0):
        if(creditScore>600):
            loan=1.2*maxEstd
            return loan
        elif(creditScore<=600 and creditScore>=581):
            loan=maxEstd
            return loan
        elif(creditScore<=580 and creditScore>=1):
            loan=0.6*maxEstd
            return loan
    elif (age>=60 and defaultFlag==1):
        if(creditScore>600):
            loan=0.9*maxEstd
            return loan
        elif(creditScore<=600 and creditScore>=581):
            loan=0.7*maxEstd
            return loan
        elif(creditScore<=580 and creditScore>=1):
            loan=0.3*maxEstd
            return loan
    print("The loan amount is:", loan)
    

def sloanapprover(loanamount,dAmount):
    if (dAmount-loanamount<0):
        print("The short term loan is:",False)
        return False
    elif (dAmount-loanamount>0):
        print("The short term loan is:",True)
        return True

def lloanapprover(loanamount,termMonths,income,defaultflag):
    ratio=(loanamount/termMonths)/income
    if (ratio<0.32 and defaultflag==0):
        print("The long term loan is:",True)
        return True
    elif (ratio<0.27 and defaultflag==1):
        print("The long term loan is:",True)
        return True
    else:
        print("The long term loan is:",False)
        return False

def interestPA(amount,termMonths,rate):
    interest=amount*(rate/100)*(termMonths/12)
    print("The interest per annum is: ",interest)
    return interest
def interestPM(amount,termMonths,rate):
    interest=(amount/termMonths)*(rate/100)
    print("The interest per month is: ",interest)
    return interest
def monthlyrepayment(amount,interest,termMonths,deposit):
    mrepayment=(amount+interest-deposit)/termMonths
    print("The monthly repayment is:",mrepayment)
    return mrepayment

#maximum amount can loan without taking into account credit score etc.
#maxEstd=predMaxamount(25,1,1,15000,1)###input is only integers###
####[[age,Number of unsecured long term across all credit providers,Number of loan repayments you have missed over the last 90 days,Income,Number of debit orders that bounced on your cheque account because of insufficient funds]]
#defaultFlag=predDefaultFlag(0,0,3,580,5)###input is only integers###
####[[weekendFlag,SalaryIndicator,Total number of credit card transactions over last 12 months,HouseholdCreditScore,NumPropertiesEverOwned]]

#final amount they can loan
#dAmount=decisionTable(25,15000,580,maxEstd,defaultFlag)

#sloan_result=(sloanapprover(30000,dAmount))
