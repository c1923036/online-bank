from django.contrib import admin
from django.contrib.flatpages import forms
from django.forms import ModelForm
from django import forms

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage

from django.forms.widgets import TextInput

from django.contrib.sites.admin import SiteAdmin
#from django.cont import SiteForm
from django.contrib.sites.models import Site

from .models import MyFlatPage, MySite

class ExtendedSiteForm(ModelForm):
    class Meta:
        model = MySite
        fields = '__all__'
        widgets = {
            'header_colour': TextInput(attrs={'type': 'color'}),
            'footer_colour': TextInput(attrs={'type': 'color'}),
            'margin_colour': TextInput(attrs={'type': 'color'}),
        }

class ExtendedSiteAdmin(SiteAdmin):
    form = ExtendedSiteForm
    fieldsets = (
        (None, {'fields': ('domain', 'name', 'bankName', 'header_colour', 'footer_colour', 'margin_colour')}),
    )




class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = MyFlatPage
        fields = '__all__'
        widgets = {
            'page_colour': TextInput(attrs={'type': 'color'}),
        }

class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'appearOnSites', 'appearOnNavbar', 'appearOnFooter', 'page_colour')}),
    )


admin.site.unregister(Site)
admin.site.register(MySite, ExtendedSiteAdmin)

admin.site.unregister(FlatPage)
admin.site.register(MyFlatPage, ExtendedFlatPageAdmin)

