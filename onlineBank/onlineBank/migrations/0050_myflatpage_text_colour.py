# Generated by Django 3.2.8 on 2022-01-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0049_mysite_title_font_colour'),
    ]

    operations = [
        migrations.AddField(
            model_name='myflatpage',
            name='text_colour',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]
