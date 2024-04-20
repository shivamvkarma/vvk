from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from store.models import Product, Variation


def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # get the product
    product_variation = []
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST :
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        is_cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0 :
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0 :
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()

        return redirect('cart:cart')

    # if the user is not authencated
    else:        

        if request.method == 'POST':
            for item in request.POST :
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        cart.save()

        is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0 :
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart=cart,
            )
            if len(product_variation) > 0 :
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()

        return redirect('cart:cart')

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else :
            cart_item.delete()
    except:
        pass

    return redirect('cart:cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart')

def cart(request, total_price=0, quantity=0, cart_items=None):
    grand_total = 0
    tax = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_price += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity
    
    except ObjectDoesNotExist:
        pass
    
    
    tax = round(((2 * total_price)/100), 2)
    grand_total = total_price + tax
    handing = 15.00
    total = float(grand_total) + handing

    context = {
        'total' : total_price,
        'quantity': quantity,
        'cart_items':cart_items,
        'order_total':total,
        'vat' : tax,
        'handing':handing,
    }

    return render(request, 'shop/cart.html', context)





from django.shortcuts import render, redirect, get_object_or_404
from .models import WishlistItem
from store.models import Product, Variation
from django.contrib import messages

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    if user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=user,
            product=product
        )
        if created:
            # If the item is added to the wishlist for the first time
            wishlist_item.variation.set(product_variation)
            wishlist_item.save()
            messages.success(request, f"{product.name} has been added to your wishlist.")
        else:
            # If the item is already in the wishlist
            messages.info(request, f"{product.name} is already in your wishlist.")
        return redirect('cart:wishlist')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('accounts:login')

def wishlist(request):
    user = request.user
    if user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=user)
        context = {
            'wishlist_items': wishlist_items
        }
        return render(request, 'shop/wishlist.html', context)
    else:
        # Redirect to login page if user is not authenticated
        return redirect('accounts:login')

def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id)
    user = request.user
    if user.is_authenticated and wishlist_item.user == user:
        product_name = wishlist_item.product.name
        wishlist_item.delete()
        messages.success(request, f"{product_name} has been removed from your wishlist.")
        return redirect('cart:wishlist')
    else:
        # Redirect to login page if user is not authenticated or doesn't own the wishlist item
        return redirect('accounts:login')
