from django.urls import path
from . import views 

app_name = 'app'

urlpatterns = [
    path('about/', views.about, name='about'),
]
