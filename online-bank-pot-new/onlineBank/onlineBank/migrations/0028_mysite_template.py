# Generated by Django 3.2.6 on 2022-01-02 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0027_outertemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysite',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineBank.outertemplate'),
        ),
    ]
