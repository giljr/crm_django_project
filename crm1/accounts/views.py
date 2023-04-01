from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import Product, Order, Customer
from accounts.form import OrderForm


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


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': ['9rnCKPAkIOMlFTn8rJzDhZE495P2b5MfRrb5DyLfxEjvPtL9z5amMA4ZokCtJIUp'],
        #              'customer': ['2'],
        #              'product': ['3'],
        #              'status': ['Delivered'],
        #               'Submit': ['Submit']}>
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
