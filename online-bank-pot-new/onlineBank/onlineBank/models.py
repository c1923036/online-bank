from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

class MySite(Site):
    bankName = models.CharField(max_length=50, default='West Midlands Regional Bank')
    header_colour = models.CharField(max_length=7, default='#096e0f')
    footer_colour = models.CharField(max_length=7, default='#096e0f')
    margin_colour = models.CharField(max_length=7, default='#FFFFFF')

class MyFlatPage(FlatPage):
    appearOnNavbar = models.BooleanField(default=False)
    appearOnFooter = models.BooleanField(default=False)
    page_colour = models.CharField(max_length=7, default='#FFFFFF')
    
    appearOnSites = models.ForeignKey(MySite, on_delete=models.CASCADE, blank=True ,null=True)
