# Generated by Django 3.2.6 on 2022-01-01 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0010_rename_colour_myflatpage_primarycolour'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myflatpage',
            old_name='primarycolour',
            new_name='primary_colour',
        ),
    ]
