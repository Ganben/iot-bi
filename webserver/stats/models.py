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
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, null=True)
    visited = models.IntegerField() # incremental counting
    status = models.BooleanField()
    first_date = models.DateField()
    last_date = models.DateTimeField(auto_now=True)

    # def inc(self):
    #     self.visited += 1
    #     # and shop's counts add too
    #     self.shop.counts += 1
    #     self.save()
    #     self.shop.save()
# livadata
class ShopDataLive(models.Model):
    #should in memory or redis
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    since = models.DateTimeField(auto_now_add=True)
    last = models.DateTimeField(auto_now=True)
    visited = models.IntegerField(default=0)
    def increment(self):
        self.visited += 1
        self.save() # optional
        
    def close(self):
        # save to month buck data
        # self.shop.counts += self.visited
        # self.shop.save()
        sm = ShopMonth(
            shop = self.shop,
            counts = self.visited
        )
        sm.save()
        self.visited = 0
        self.save()

class DeviceDataLive(models.Model):
    shop = models.ForeignKey(ShopDataLive, on_delete=models.DO_NOTHING)
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    visited = models.IntegerField(default=0)
    
    def increment(self):
        # live method
        self.visited += 1
        self.shop.visited += 1
        self.save()
        self.shop.save()
    
    def close(self):
        # reset visited
        dm = DeviceMonth(
            device=self.device,
            counts = self.visited
        )
        dm.save()
        self.visited = 0
        self.save()

class ShopMonth(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, null=True)
    month = models.DateField(auto_now_add=True)
    counts = models.IntegerField(default=0)

class DeviceMonth(models.Model):
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING, null=True)
    month = models.DateField(auto_now_add=True)
    counts = models.IntegerField(default=0)
