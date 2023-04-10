from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import Product, Order, Customer
from accounts.form import CustomerForm, OrderForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.decorators import is_user_auth_decorator, is_user_allow_decorator, is_user_admin_decorator
from django.contrib.auth.models import Group


@login_required(login_url='login')
# @is_user_allow_decorator(allowed_roles=['admin'])
@is_user_admin_decorator
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


@login_required(login_url='login')
@is_user_allow_decorator(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@is_user_allow_decorator(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', context={'products': products})
    # return HttpResponse('Products')


@login_required(login_url='login')
@is_user_allow_decorator(allowed_roles=['admin'])
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


@login_required(login_url='login')
@is_user_allow_decorator(allowed_roles=['admin'])
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


@login_required(login_url='login')
@is_user_allow_decorator(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@is_user_auth_decorator
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            # Added username because of error returning customer name if not added
            Customer.objects.create(user=user, name=user.username,)

            messages.success(
                request, 'Account created successfully for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@is_user_auth_decorator
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect!')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@is_user_allow_decorator(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@is_user_allow_decorator(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders)

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)
