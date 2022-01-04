from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import string, random

class innerTemplate(models.Model):
    name = models.CharField(
        max_length=50, default='template.html', primary_key=True)
    file = models.FileField(upload_to='onlineBank/templates/flatpages')


class outerTemplate(models.Model):
    name = models.CharField(
        max_length=50, default='template.html', primary_key=True)
    file = models.FileField(upload_to='onlineBank/templates')


class logo(models.Model):
    name = models.CharField(max_length=50, default='', primary_key=True)
    file = models.FileField(upload_to='onlineBank/static/logo')


class staticFile(models.Model):
    name = models.CharField(max_length=50, default='', primary_key=True)
    file = models.FileField(upload_to='onlineBank/static')


class MySite(Site):
    bankName = models.CharField(
        max_length=50, default='West Midlands Regional Bank')
    header_colour = models.CharField(max_length=7, default='#096e0f')
    footer_colour = models.CharField(max_length=7, default='#096e0f')
    margin_colour = models.CharField(max_length=7, default='#FFFFFF')
    template = models.ForeignKey(
        outerTemplate, blank=True, null=True, on_delete=models.SET_NULL)
    logo = models.ForeignKey(
        logo, blank=True, null=True, on_delete=models.SET_NULL)


class MyFlatPage(FlatPage):
    appearOnNavbar = models.BooleanField(default=False)
    appearOnFooter = models.BooleanField(default=False)
    page_colour = models.CharField(max_length=7, default='#FFFFFF')
    appearOnSites = models.ForeignKey(
        MySite, on_delete=models.CASCADE, blank=True, null=True)
    template = models.ForeignKey(
        innerTemplate, blank=True, null=True, on_delete=models.SET_NULL)

def pkgen():
    letters = string.digits
    return ( ''.join(random.choice(letters) for i in range(8)) )


class account(models.Model):
    accountNumber = models.CharField(max_length=8, primary_key=True, default=pkgen)
    accountOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    accountName = models.CharField(max_length=20, default="Current Account")
    accountBalance = models.DecimalField(max_digits=10, decimal_places=2)
    accountSortCode = models.CharField(max_length=8, null=True, blank=True)



