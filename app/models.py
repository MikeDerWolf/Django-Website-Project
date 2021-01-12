from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=50, error_messages={'required': 'This field is required',
                                                           'invalid': 'Name has maximum 50 characters!'
                                                           })
    description = models.CharField(max_length=300, error_messages={'required': 'This field is required',
                                                                   'invalid': 'Description has maximum 300 characters!'
                                                                   })
    price = models.FloatField(error_messages={'required': 'This field is required'})
    stock = models.PositiveIntegerField(error_messages={'required': 'This field is required',
                                                        'invalid': 'Stock must be greater or equal to 0!'
                                                        })
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyerProfile', primary_key=True)
    address = models.CharField(max_length=100, error_messages={'required': 'This field is required',
                                                               'invalid': 'Adress has maximum 100 characters!'
                                                               })
    role = models.CharField(max_length=10, default='buyer', editable=False)
    orders = models.ManyToManyField(Product, through='Order')


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sellerProfile', primary_key=True)
    telephone = models.CharField(max_length=10, error_messages={'required': 'This field is required',
                                                                'invalid': 'Telephone number has maximum 10 digits!'
                                                                })
    country = models.CharField(max_length=50, error_messages={'required': 'This field is required',
                                                              'invalid': 'Country has maximum 50 characters!'
                                                              })
    role = models.CharField(max_length=10, default='seller', editable=False)


class Order(models.Model):
    user = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    noOfPcs = models.PositiveIntegerField(error_messages={'required': 'This field is required'})
    total = models.FloatField(error_messages={'required': 'This field is required'})
    date = models.DateField()
    shippingAddress = models.CharField(max_length=100, error_messages={'required': 'This field is required',
                                                                       'invalid': 'Shipping address has maximum 100 '
                                                                                  'characters! '
                                                                       })
    status = models.CharField(max_length=15, default="IN PROGRESS")



