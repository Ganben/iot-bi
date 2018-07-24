from django.urls import path
from django.urls import include

from stats import (
    views,
)

urlpatterns = [
    path('detail/<int:shopid>/', views.ShopDetail.as_view(), name='shop'),
    path('', views.index, name='index'),
]
