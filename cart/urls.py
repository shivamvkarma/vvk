from django.urls import path
from . import views 

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/<int:product_id>/add', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/<int:item_id>/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),

]
