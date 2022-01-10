# Generated by Django 3.2.6 on 2022-01-02 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0021_auto_20220102_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='innerTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='template.html', max_length=50)),
                ('file', models.FileField(upload_to='static/templates/flatpages')),
            ],
        ),
    ]