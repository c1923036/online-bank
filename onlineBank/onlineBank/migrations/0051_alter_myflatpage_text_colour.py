# Generated by Django 3.2.8 on 2022-01-19 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0050_myflatpage_text_colour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myflatpage',
            name='text_colour',
            field=models.CharField(default='#000000', max_length=7),
        ),
    ]
