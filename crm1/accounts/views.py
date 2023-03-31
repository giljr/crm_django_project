from django.http import HttpResponse
from django.shortcuts import render
from accounts.models import Product, Order, Customer


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)
    # return HttpResponse('Home')


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    # quering child from model field
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders}
    return render(request, 'accounts/customer.html', context)
    # return HttpResponse('Customer')


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', context={'products': products})
    # return HttpResponse('Products')
