from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from onlineBank.models import MySite, MyFlatPage, account, transaction, ip
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from onlineBank.arguments import createArgs, getSite
#from django.shortcuts import render_to_response
from django.template import RequestContext
import os
from datetime import datetime
import re


def confirmation(request, accountNum, amount=None, payeeAccountNum=None, payeeAccountSort=None, reference=None):
    userAccount = account.objects.get(accountNumber=accountNum)
    if request.method == 'POST' and (request.path == '/payment/' + accountNum or request.path == '/transfer/' + accountNum):
        userAccount = account.objects.get(accountNumber=accountNum)
        args = createArgs(request)
        args['amount'] = amount
        args['payeeAccountNum'] = payeeAccountNum
        args['payeeAccountSort'] = payeeAccountSort
        args['reference'] = reference
        return render(request, 'confirmation.html', args)
    elif request.method == 'POST' and request.path == '/confirmation/' + accountNum:
        amount = float(request.POST['currency-field'])
        transfer = transaction.objects.create(account=userAccount, otherAccountNumber=request.POST['payeeAccountNum'], otherSortCode=request.POST['payeeAccountSort'], withdrawal=True, amount=amount, date=datetime.today(), reference=request.POST['reference'], type="BACS", newBalance=float(userAccount.accountBalance) - amount)
        transfer.save()  #Saves created transaction data object.
        userAccount.accountBalance = float(userAccount.accountBalance) - amount
        userAccount.save()  #Saves users account with updated balance.
        
        recipientAccount = account.objects.filter(accountNumber=request.POST['payeeAccountNum']).exists()
        if recipientAccount != False:
            recipientAccount = account.objects.get(accountNumber=request.POST['payeeAccountNum'])
            recipientAccount.accountBalance = float(recipientAccount.accountBalance) + amount  #Updates the recipient account balance.
            recipientAccount.save()
            recipientTransaction = transaction.objects.create(account=recipientAccount, otherAccountNumber=userAccount.accountNumber, withdrawal=False, amount=amount, date=datetime.today(), reference=request.POST['reference'], type="BACS", newBalance=float(recipientAccount.accountBalance))
            recipientTransaction.save()  #Adds a transaction object belonging to the recipient.

        return JsonResponse({'redirect': '/accounts/'}, status=200)


def user_login(request):
    site = getSite(request)
    if site == None:
        return
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #login(request, user)
            # Redirect to index page.
            if site.malwareDeployment == True:
                return JsonResponse({"success": True}, status=200)
            else:
                login(request, user)
                return JsonResponse({'redirect': '/accounts/'}, status=200)
        else:
            # Return an 'invalid login' error message.
            print("invalid login details " + username + " " + password)
            return render(request, 'registration/login.html')
    else:
        args = createArgs(request)
        # the login is a  GET request, so just show the user the login form.
        return render(request, 'registration/login.html', args)

def accounts(request):
    """Returns the accounts page"""
    if request.user.is_authenticated == True:
        args = createArgs(request)

        return render(request, 'accounts.html', args)

    else:
        return redirect('/login/')


def statement(request, accountNum):
    """Returns the bank statement for the selected account"""
    if request.user.is_authenticated == True:  #Checks the user is appropriately authenticated.
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:  #Checks the account number belongs to the authenticated user.

            args = createArgs(request)
            
            return render(request, 'statement.html', args)
    else:
        return redirect('/login/')    


def transfer(request, accountNum):
    """Returns the user a form to make a transfer between a users accounts and then handles form submission"""
    if request.user.is_authenticated == True:  #Checks user is authenticated.
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:  #Checks account belongs to authenticated user.
            if request.method == 'GET':  #If GET request returns the render of the form.
                args = createArgs(request)

                return render(request, 'transfer.html', args)
            
            elif request.method == "POST":  #If POST request handles input data and inserts to the database.
                return confirmation(request, accountNum, amount=float(request.POST['currency-field'][1:].replace(',', '')), payeeAccountNum=request.POST['accountNumber'], payeeAccountSort=account.objects.get(accountNumber=accountNum).accountSortCode, reference=request.POST["reference"])
        
    else:
        return redirect('/login/')  #If not authenticated user is returned to the log in page.

def payment(request, accountNum):
    """Returns the user a form to make a transfer between a users accounts and then handles form submission"""
    if request.user.is_authenticated == True:  #If user is authenticated.
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:  #Checks account belongs to authenticated user.
            if request.method == 'GET':  #If GET request returns the render of the form.                
                args = createArgs(request)
                return render(request, 'payment.html', args)
            
            elif request.method == "POST":  #If a POST request.

                return confirmation(request, accountNum, amount=float(request.POST['currency-field'][1:].replace(',', '')), payeeAccountNum=request.POST['accountNumber'], payeeAccountSort=request.POST['sort-code'], reference=request.POST["reference"])
    
    else:
        return redirect('/login/')

def profile(request):
    """Returns the profile page"""
    if request.user.is_authenticated == True:
        args = createArgs(request)

        return render(request, 'profile.html', args)

    else:
        return redirect('/login/')     