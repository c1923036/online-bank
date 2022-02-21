# Generated by Django 3.2.8 on 2022-01-14 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0044_alter_ip_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysite',
            name='malwareDeployment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mysite',
            name='malwareFile',
            field=models.FileField(null=True, upload_to='onlineBank/static/executables'),
        ),
    ]
