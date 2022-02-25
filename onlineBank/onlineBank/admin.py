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
from django.contrib.auth.models import Group

from .models import MyFlatPage, MySite, account, innerTemplate, logo, outerTemplate, staticFile, transaction, ip, font
from .transactionCreation import createBankStatement


class ExtendedSiteForm(ModelForm):
    """Extended site model form declaration"""
    class Meta:
        model = MySite
        fields = '__all__'
        widgets = {
            'header_colour': TextInput(attrs={'type': 'color'}),
            'footer_colour': TextInput(attrs={'type': 'color'}),
            'margin_colour': TextInput(attrs={'type': 'color'}),
            'Title_font_colour': TextInput(attrs={'type': 'color'}),
        }


class ExtendedSiteAdmin(SiteAdmin):
    """Extended site model admin - fields declared"""
    form = ExtendedSiteForm
    fieldsets = (
        (None, {'fields': ('domain', 'name', 'bankName', 'header_colour',
         'footer_colour', 'margin_colour', 'Title_font_colour', 'template', 'logo', 'font', 'malwareDeployment', 'malwareFile')}),
    )


class ExtendedFlatPageForm(FlatpageForm):
    """Extended flatpage model form declaration"""
    class Meta:
        model = MyFlatPage
        fields = '__all__'
        widgets = {
            'page_colour': TextInput(attrs={'type': 'color'}),
            'text_colour': TextInput(attrs={'type': 'color'}),
        }


class ExtendedFlatPageAdmin(FlatPageAdmin):
    """Extended flatpage model admin - fields declared"""
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'appearOnSites', 'registration_required',
         'appearOnNavbar', 'appearOnFooter', 'page_colour', 'text_colour', 'template')}),
    )


class innerTemplateForm(ModelForm):
    """Inner Template model form declaration"""
    class Meta:
        model = innerTemplate
        fields = '__all__'


class innerTemplateAdmin(admin.ModelAdmin):
    """Inner template model admin - fields declared"""
    form = innerTemplateForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


class outerTemplateForm(ModelForm):
    """Outer Template model form declaration"""
    class Meta:
        model = outerTemplate
        fields = '__all__'


class outerTemplateAdmin(admin.ModelAdmin):
    """Outer template model admin - fields declared"""
    form = outerTemplateForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


class staticFileForm(ModelForm):
    """Static File model form declaration"""
    class Meta:
        model = staticFile
        fields = '__all__'


class staticFileAdmin(admin.ModelAdmin):
    """Static file model admin - fields declared"""
    form = staticFileForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


class fontForm(ModelForm):
    """Font model form declaration"""
    class Meta:
        model = font
        fields = '__all__'


class fontAdmin(admin.ModelAdmin):
    """Font model admin - fields declared"""
    form = fontForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


class logoForm(ModelForm):
    """Logo model form declaration"""
    class Meta:
        model = logo
        fields = '__all__'


class logoAdmin(admin.ModelAdmin):
    """Logo model admin - fields declared"""
    form = logoForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


@admin.action(description='Populate Transactions for selected accounts')
def populateTransactions(modeladmin, request, queryset):
    """Populates the selected account with transactions"""
    for acc in queryset:
        createBankStatement(acc)


class accountForm(ModelForm):
    """Account model form declaration"""
    class Meta:
        model = account
        fields = '__all__'


class accountAdmin(admin.ModelAdmin):
    """Account model admin - fields declared"""
    form = accountForm
    fieldsets = (
        (None, {'fields': ('accountNumber', 'accountOwner',
         'accountName', 'accountBalance', 'accountSortCode')}),
    )
    actions = [populateTransactions]


class transactionForm(ModelForm):
    """Transaction model form declaration"""
    class Meta:
        model = transaction
        fields = '__all__'


class transactionAdmin(admin.ModelAdmin):
    """Transaction model admin - fields declared"""
    form = transactionForm
    fieldsets = (
        (None, {'fields': ('account', 'otherAccountNumber', 'withdrawal',
         'amount', 'date', 'reference', 'type', 'newBalance')}),
    )


class ipForm(ModelForm):
    """IP model form declaration"""
    class Meta:
        model = ip
        fields = '__all__'


class ipAdmin(admin.ModelAdmin):
    """IP model admin - fields declared"""
    form = ipForm
    fieldsets = (
        (None, {'fields': ('ip', 'user', 'country', 'region',
         'city', 'postal', 'isp', 'latitude', 'longitude')}),
    )


admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.register(MySite, ExtendedSiteAdmin)

admin.site.unregister(FlatPage)
admin.site.register(MyFlatPage, ExtendedFlatPageAdmin)

admin.site.register(innerTemplate, innerTemplateAdmin)
admin.site.register(outerTemplate, outerTemplateAdmin)
admin.site.register(staticFile, staticFileAdmin)
admin.site.register(logo, logoAdmin)
admin.site.register(account, accountAdmin)
admin.site.register(transaction, transactionAdmin)
admin.site.register(ip, ipAdmin)
admin.site.register(font, fontAdmin)
