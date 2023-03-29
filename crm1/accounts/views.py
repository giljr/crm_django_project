from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'accounts/dashboard.html')
    # return HttpResponse('Home')


def customer(request):
    return render(request, 'accounts/customer.html')
    # return HttpResponse('Customer')


def products(request):
    return render(request, 'accounts/products.html')
    # return HttpResponse('Products')
