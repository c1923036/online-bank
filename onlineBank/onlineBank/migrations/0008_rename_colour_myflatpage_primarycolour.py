# Generated by Django 3.2.6 on 2022-01-01 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0007_rename_color_myflatpage_colour'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myflatpage',
            old_name='colour',
            new_name='primarycolour',
        ),
    ]
