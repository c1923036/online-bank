# Generated by Django 3.2.6 on 2022-01-02 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0025_alter_innertemplate_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='myflatpage',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineBank.innertemplate'),
        ),
    ]
