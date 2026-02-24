from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
]
