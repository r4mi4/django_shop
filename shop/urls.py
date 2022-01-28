from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('category/<slug:slug>/', views.shop, name='category_filter'),
    path('manufacturer/<slug:slug>/', views.shop, name='manufacturer_filter'),
    path('product_details/<slug:slug>/', views.product_details, name='product'),
]
