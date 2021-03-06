from distutils.command.upload import upload
from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import string
import random
import zipfile


class innerTemplate(models.Model):
    """Declaration of inner template model"""
    name = models.CharField(
        max_length=50, default='template.html', primary_key=True)
    file = models.FileField(upload_to='onlineBank/templates/flatpages')


class outerTemplate(models.Model):
    """Declaration of outer template model"""
    name = models.CharField(
        max_length=50, default='template.html', primary_key=True)
    file = models.FileField(upload_to='onlineBank/templates')


class logo(models.Model):
    """Declaration of logo model"""
    name = models.CharField(max_length=50, default='', primary_key=True)
    file = models.FileField(upload_to='onlineBank/static/logo')


class staticFile(models.Model):
    """Declaration of static file model"""
    name = models.CharField(max_length=50, default='', primary_key=True)
    file = models.FileField(upload_to='onlineBank/static')


class font(models.Model):
    """Declaration of font model"""
    name = models.CharField(max_length=50, default='', primary_key=True)
    file = models.FileField(upload_to='onlineBank/static/fonts')

    def save(self, *args, **kwargs):
        """Overriding save method of font to extract zip files"""
        with zipfile.ZipFile(self.file, 'r') as zip_ref:
            zip_ref.extractall(self.file.field.upload_to)
        return super(font, self).save(*args, **kwargs)


class MySite(Site):
    """Declaration of extended Site model"""
    domain_value = models.CharField(max_length=100, blank=True, null=True)
    bankName = models.CharField(
        max_length=50, default='West Midlands Regional Bank')
    header_colour = models.CharField(max_length=7, default='#096e0f')
    footer_colour = models.CharField(max_length=7, default='#096e0f')
    margin_colour = models.CharField(max_length=7, default='#FFFFFF')
    Title_font_colour = models.CharField(max_length=7, default='#FFFFFF')
    template = models.ForeignKey(
        outerTemplate, blank=True, null=True, on_delete=models.SET_NULL)
    logo = models.ForeignKey(
        logo, blank=True, null=True, on_delete=models.SET_NULL)
    font = models.ForeignKey(
        font, blank=True, null=True, on_delete=models.SET_NULL)
    malwareDeployment = models.BooleanField(default=False)
    malwareFile = models.FileField(
        upload_to='static/executables', null=True, blank=True)


class MyFlatPage(FlatPage):
    """Declaration of extended flatpage model"""
    appearOnNavbar = models.BooleanField(default=False)
    appearOnFooter = models.BooleanField(default=False)
    page_colour = models.CharField(max_length=7, default='#FFFFFF')
    text_colour = models.CharField(max_length=7, default='#000000')
    appearOnSites = models.ForeignKey(
        MySite, on_delete=models.CASCADE, blank=True, null=True)
    template = models.ForeignKey(
        innerTemplate, blank=True, null=True, on_delete=models.SET_NULL)


def pkgen():
    """Function to randomly generate account numbers"""
    letters = string.digits
    return (''.join(random.choice(letters) for i in range(8)))


class account(models.Model):
    """Declaration of account model"""
    accountNumber = models.CharField(
        max_length=8, primary_key=True, default=pkgen)
    accountOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    accountName = models.CharField(max_length=20, default="Current Account")
    accountBalance = models.DecimalField(max_digits=10, decimal_places=2)
    accountSortCode = models.CharField(max_length=8, null=True, blank=True)


class transaction(models.Model):
    """Declaration of transaction model"""
    account = models.ForeignKey(account, on_delete=models.CASCADE)
    otherAccountNumber = models.CharField(max_length=8, null=True, blank=True)
    otherSortCode = models.CharField(max_length=8, null=True, blank=True)
    withdrawal = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=40, default="")
    reference = models.CharField(max_length=20, default="")
    type = models.CharField(max_length=10, default="")
    newBalance = models.DecimalField(max_digits=10, decimal_places=2)


class ip(models.Model):
    """Declaration of IP model"""
    ip = models.CharField(max_length=15)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=15, null=True)
    region = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=15, null=True)
    postal = models.CharField(max_length=5, null=True)
    isp = models.CharField(max_length=50, null=True)
    latitude = models.CharField(max_length=8, null=True)
    longitude = models.CharField(max_length=8, null=True)
