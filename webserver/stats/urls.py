from django.urls import path

from stats import (
    views,
)

urlpatterns = [
    path('detail', views.ShopDetail.as_view(), name='shop'),
    path('', views.index, name='index'),
]
