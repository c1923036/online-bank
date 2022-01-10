# Generated by Django 3.2.6 on 2022-01-05 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0035_account_accountsortcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otherAccountNumber', models.CharField(blank=True, max_length=8, null=True)),
                ('withdrawal', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('reference', models.CharField(default='', max_length=20)),
                ('type', models.CharField(default='', max_length=10)),
                ('newBalance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineBank.account')),
            ],
        ),
    ]