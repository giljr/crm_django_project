from accounts import views
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('customer/', views.customer),
    path('products/', views.products)
]
