# Generated by Django 3.2.6 on 2022-01-02 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineBank', '0026_myflatpage_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='outerTemplate',
            fields=[
                ('name', models.CharField(default='template.html', max_length=50, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='onlineBank/templates')),
            ],
        ),
    ]
