# Generated by Django 3.2.6 on 2022-01-01 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
        ('onlineBank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navbarcontent',
            name='page',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='flatpages.flatpage', verbose_name='Page Name'),
        ),
    ]
