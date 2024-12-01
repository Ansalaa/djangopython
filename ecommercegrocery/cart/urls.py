"""
URL configuration for ecommercegrocery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from cart import views

app_name="cart"

urlpatterns = [
    path('<int:i>',views.addcart,name="addcart"),
    path('cartview',views.cart_view,name="cartview"),
    path('cart_remove/<int:i>',views.cart_remove,name="cart_remove"),
    path('cart_delete/<int:i>', views.cart_delete, name="cart_delete"),
    path('orderform',views.orderform,name="orderform"),
    path('payment_status/<str:p>', views.payment_status, name='payment_status'),
    path('orderview',views.orderview,name="orderview")
]