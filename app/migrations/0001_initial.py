# Generated by Django 3.1.5 on 2021-01-13 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='buyerProfile', serialize=False, to='auth.user')),
                ('address', models.CharField(error_messages={'invalid': 'Adress has maximum 100 characters!', 'required': 'This field is required'}, max_length=100)),
                ('role', models.CharField(default='buyer', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='sellerProfile', serialize=False, to='auth.user')),
                ('telephone', models.CharField(error_messages={'invalid': 'Telephone number has maximum 10 digits!', 'required': 'This field is required'}, max_length=10)),
                ('country', models.CharField(error_messages={'invalid': 'Country has maximum 50 characters!', 'required': 'This field is required'}, max_length=50)),
                ('role', models.CharField(default='seller', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'invalid': 'Name has maximum 50 characters!', 'required': 'This field is required'}, max_length=50)),
                ('description', models.CharField(error_messages={'invalid': 'Description has maximum 300 characters!', 'required': 'This field is required'}, max_length=300)),
                ('price', models.FloatField(error_messages={'required': 'This field is required'})),
                ('stock', models.PositiveIntegerField(error_messages={'invalid': 'Stock must be greater or equal to 0!', 'required': 'This field is required'})),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noOfPcs', models.PositiveIntegerField(error_messages={'required': 'This field is required'})),
                ('total', models.FloatField(error_messages={'required': 'This field is required'})),
                ('date', models.DateField()),
                ('shippingAddress', models.CharField(error_messages={'invalid': 'Shipping address has maximum 100 characters! ', 'required': 'This field is required'}, max_length=100)),
                ('status', models.CharField(default='IN PROGRESS', max_length=15)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.buyerprofile')),
            ],
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='orders',
            field=models.ManyToManyField(through='app.Order', to='app.Product'),
        ),
    ]