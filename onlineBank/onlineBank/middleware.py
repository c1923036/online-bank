from onlineBank.models import MyFlatPage, outerTemplate, ip
from onlineBank.models import MySite
from onlineBank.settings import NAVBAR_CONSTANTS
import os
import ipinfo
from django.shortcuts import render


class myFlatpages:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Returns flatpage render if necessary
        
        If the current response is due to be a 404 error the request is checked to see if it is for one of the user created flatpages.  If this is the case the page will be rendered.
        """
        recordAccess(request)
        response = self.get_response(request)
        if response.status_code == 404:  #Checks for 404 error.
            pages = MyFlatPage.objects.all()
            for page in pages:
                if page.url == request.path and (page.registration_required != True or request.user.is_authenticated == True):  #Checks if the page has been rendered. Also checks if authentication is necessary, if so authentication is checked.
                    site = page.appearOnSites  #Gets the page's site.
                    if page.template != None:
                        innerTemplate = page.template.file.path
                    else:
                        innerTemplate = "flatpages/default.html"  #Default inner template value assigned if null.
                    if site.template != None:
                        outerTemplate = site.template.file.path
                    else:
                        outerTemplate = "template.html"  #Default outer template value assigned if null.
                    if site.logo != None:
                        logo = os.path.relpath(
                            site.logo.file.url, '/onlineBank/static')  #Creates correct site logo path.
                    else:
                        logo = None

                    if site.font != None:
                        font = os.path.relpath(
                            site.font.file.url, '/onlineBank/static')
                        font = font.replace('.zip', '')
                        font += '-regular'

                    navbarContents = getNavBarContents(pages)  #Returns the names and links to feature on the navbar.
                    footerContents = getFooterContents(pages)  #Returns the names and links to feature on the footer.

                    navbarContents = removeUnneccessaryContents(navbarContents, request.user.is_authenticated)  #Removes login or logout when the user is logged in or logged out respectively.

                    args = {'flatpage': page, 'navbarContents': navbarContents, 'footerContents': footerContents,
                            'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'font': font}  #Constructs arguments dictionary to be passed
                    response = render(request, innerTemplate, args)
        return response


def getNavBarContents(pages):
    """Returns an array of dictionary objects containing the navbar contents"""
    navbarContents = []
    navbarContents += NAVBAR_CONSTANTS
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

def removeUnneccessaryContents(navbarContents, loggedIn):
    """Returns navbar contents minus the login or logout object depending on if the user is logged in or logged out"""
    for i in range(0, len(navbarContents)):
        if loggedIn == True and navbarContents[i]['url'] == "/login":
            navbarContents.pop(i)
            return navbarContents
        elif loggedIn == False and navbarContents[i]['url'] == "/logout":
            navbarContents.pop(i)
            return navbarContents
    return navbarContents


def recordAccess(request):
    requestIP = get_client_ip(request)
    alreadyGot = list(ip.objects.filter(ip=requestIP))
    for i in range(len(alreadyGot)):
        if alreadyGot[i].user == request.user:
            return
    ipDetails = resolveIP(requestIP)
    record = createRecord(requestIP, request.user, ipDetails)
    record.save()
    return

def createRecord(requestIP, user, ipDetails):
    record = ip()
    record.ip = requestIP
    if user.is_anonymous != True:
        record.user = user
    if 'country' in ipDetails:
        record.country = ipDetails['country']
    if 'region' in ipDetails:
        record.region = ipDetails['region']
    if 'city' in ipDetails:
        record.city = ipDetails['city']
    if 'postal' in ipDetails:
        record.postal = ipDetails['postal']
    if 'org' in ipDetails:
        record.isp = ipDetails['org']
    if 'latitude' in ipDetails:
        record.latitude = ipDetails['latitude']
    if 'longitude' in ipDetails:
        record.longitude = ipDetails['longitude']
    return record



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def resolveIP(ip):
    access_token = '6f4b955ad955d1'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip)
    return details.all