from django.urls import path
from django.utils.regex_helper import normalize
from . import views
from django.conf.urls import handler404


app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    # path('shop/', views.shop, name='shop'),
    # path('shop/<slug:category_slug>/', views.shop, name='categries'),
    # path('shop/<slug:category_slug>/<slug:product_details_slug>/', views.product_details, name='product_details'),
    # path('search/', views.search, name='search'),
    # path('review/<int:product_id>/', views.review, name='review'),
]


handler404 = 'store.views.error_404_view'

