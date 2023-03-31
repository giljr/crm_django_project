from accounts import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('products/', views.products, name="products"),
]
