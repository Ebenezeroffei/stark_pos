# Generated by Django 3.1.7 on 2021-04-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20210402_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetails',
            name='image',
            field=models.ImageField(default='company_logo.png', upload_to='company_logo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_logo.png', upload_to='product_images'),
        ),
    ]
