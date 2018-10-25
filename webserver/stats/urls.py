from django.urls import path
from django.urls import include

from stats import (
    views,
)

urlpatterns = [
    path('detail/<int:shopid>/', views.ShopDetail.as_view(), name='shop'),
    path('dev/<int:device>/', views.DeviceView.as_view(), name = 'device'),
    path('', views.index, name='index'),
]
