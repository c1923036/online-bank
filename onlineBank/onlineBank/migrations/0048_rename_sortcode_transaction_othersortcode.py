# Generated by Django 3.2.8 on 2022-01-18 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0047_transaction_sortcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='sortCode',
            new_name='otherSortCode',
        ),
    ]
