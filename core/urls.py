from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('company.urls', namespace='company')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
]

