# Generated by Django 3.0.8 on 2020-10-21 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20201021_0856'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productdata',
            options={'ordering': ['date']},
        ),
    ]
