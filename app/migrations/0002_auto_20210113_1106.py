# Generated by Django 3.1.5 on 2021-01-13 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyerprofile',
            name='role',
            field=models.CharField(default='buyer', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='role',
            field=models.CharField(default='seller', editable=False, max_length=10),
        ),
    ]