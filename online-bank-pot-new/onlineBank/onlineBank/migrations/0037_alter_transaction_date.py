# Generated by Django 3.2.6 on 2022-01-05 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0036_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.CharField(default='', max_length=40),
        ),
    ]
