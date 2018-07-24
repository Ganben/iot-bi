from django.contrib import admin
from stats.models import (
    Shop,
    ShopDataLive,
    Device,
    DeviceDataLive,
)
# Register your models here.

admin.site.register(Shop)
admin.site.register(ShopDataLive)

admin.site.register(Device)
admin.site.register(DeviceDataLive)

