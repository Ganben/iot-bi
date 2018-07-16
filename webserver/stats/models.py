from django.db import models

# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=20)
    firstset = models.DateField()
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    mobilephone = models.CharField(max_length=15)

class Device(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    visited = models.IntegerField()
    status = models.BooleanField()
    first_date = models.DateField()
    last_date = models.DateTimeField(auto_now=True)

