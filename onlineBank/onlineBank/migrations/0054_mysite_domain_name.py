# Generated by Django 3.2.6 on 2022-01-22 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0053_mysite_font'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysite',
            name='domain_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
