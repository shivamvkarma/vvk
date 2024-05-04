from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import BannerContent, Product, Category
from cart.views import _cart_id
from cart.models import CartItem
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from .models import ProductGallery
from app.models import InstagramImage, SubBanners

def home(request):
    banner_contents = BannerContent.objects.all()
    sub_banners = SubBanners.objects.all()
    instagram_images = InstagramImage.objects.all()
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    
    context = {
        'products' : products,
        'categories': categories,
        'sub_banners': sub_banners,
        'banner_contents': banner_contents,
        'instagram_images': instagram_images,
    }
    return render(request, 'index.html', context)




from django.db.models import Q

def shop(request, category_slug=None):
    categories = None
    products = None

    # Filter products based on category
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    # Apply filters from the request
    size_filter_values = request.GET.getlist('size')
    color_filter_values = request.GET.getlist('color')
    gender_filter_values = request.GET.getlist('gender')

    # if gender:
    #     products = products.filter(gender__icontains=gender)

    # Initialize the products queryset
    products = Product.objects.all()

    # Apply size filters
    if size_filter_values:
        size_filters = Q()
        for size in size_filter_values:
            size_filters |= Q(variation__variation_category='size', variation__variation_value__iexact=size)
        products = products.filter(size_filters).distinct()

    # Apply color filters
    if color_filter_values:
        color_filters = Q()
        for color in color_filter_values:
            color_filters |= Q(variation__variation_category='color', variation__variation_value__iexact=color)
        products = products.filter(color_filters).distinct()
    
    # Sorting
    sort_option = request.GET.get('sort')
    if sort_option == 'price_low_to_high':
        products = products.order_by('selling_price')
    elif sort_option == 'price_high_to_low':
        products = products.order_by('-selling_price')

    # if gender_filter_values:
    #     products = products.filter(gender__in=gender_filter_values)

    # Ensure distinct results
    products = products.distinct()

    # Pagination
    paginator = Paginator(products, 100)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    products_count = products.count()

    context = {
        'category_slug': category_slug,
        'products': paged_products,
        'products_count': products_count,
        'size_filter_values': size_filter_values,
        'color_filter_values': color_filter_values,
        'gender_filter_values': gender_filter_values

    }
    return render(request, 'shop/shop.html', context)


def product_details(request, category_slug, product_details_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_details_slug)
        related_products = Product.objects.filter(category__slug=category_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        return e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.order_by('-updated_at').filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct':orderproduct,
        'related_products':related_products,
        'reviews': reviews,
        'product_gallery':product_gallery,
    }
    return render(request, 'shop/product_detail.html', context)


def search(request):
    print("IN SERARCH ")
    products_count = 0
    products = None
    paged_products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword :
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            
            products_count = products.count()
            
    
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'shop/search.html', context)



def review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, your review updated!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, your review Posted!')
                return redirect(url)

