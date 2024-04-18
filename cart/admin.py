from django.contrib import admin
from .models import Cart, CartItem, WishlistItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'create']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product','cart', 'quantity', 'is_active']

admin.site.register(WishlistItem)