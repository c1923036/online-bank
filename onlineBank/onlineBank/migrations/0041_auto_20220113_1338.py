# Generated by Django 3.2.8 on 2022-01-13 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0040_alter_ip_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='city',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='region',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
