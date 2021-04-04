from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from multiselectfield import MultiSelectField


class ProductDet(models.Model):
    product_image = models.ImageField()
    product_name = models.CharField(max_length=50)
    product_id = models.BigIntegerField(unique=True)


class Address(models.Model):
    product_det = models.ForeignKey(ProductDet,default=0, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=150)
    # phone = models.CharField(max_length=150)
    phone_number = PhoneNumberField()
    city = models.CharField(max_length=150)
    pin_code =  models.BigIntegerField()
    MY_CHOICES = (
        (1,"XS"),
        (2,"S"),
        (3,"M"),
        (4,"L"),
        (5,"XL"),
        (6,"XXL"),
    )
    latitude = models.CharField(max_length=9, default='29.976480')
    longitude = models.CharField(max_length=9, default='31.131302')
    size = MultiSelectField(choices=MY_CHOICES, max_choices=6, default="S")
