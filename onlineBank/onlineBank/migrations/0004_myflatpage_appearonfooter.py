# Generated by Django 3.2.6 on 2022-01-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0003_auto_20220101_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='myflatpage',
            name='appearOnFooter',
            field=models.BooleanField(default=False),
        ),
    ]
