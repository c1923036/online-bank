# Generated by Django 3.2.6 on 2022-01-01 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0012_auto_20220101_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='myflatpage',
            name='page_colour',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]
