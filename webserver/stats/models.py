from django.db import models

# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=20)
    firstset = models.DateField()
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    units = models.IntegerField()
    counts = models.IntegerField()
    mobilephone = models.CharField(max_length=15)

class Device(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    visited = models.IntegerField() # incremental counting
    status = models.BooleanField()
    first_date = models.DateField()
    last_date = models.DateTimeField(auto_now=True)

    def inc(self):
        self.visited += 1
        # and shop's counts add too
        self.shop.counts += 1
        self.save()
        self.shop.save()
