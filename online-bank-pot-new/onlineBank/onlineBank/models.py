from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage

class MyFlatPage(FlatPage):
    appearOnNavbar = models.BooleanField(default=False)
    appearOnFooter = models.BooleanField(default=False)
    header_colour = models.CharField(max_length=7, default='#096e0f')
    footer_colour = models.CharField(max_length=7, default='#096e0f')
    page_colour = models.CharField(max_length=7, default='#FFFFFF')
    margin_colour = models.CharField(max_length=7, default='#FFFFFF')

    


#admin.site.register(MyFlatPage)
#admin.site.unregister(FlatPage)