from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import Product, Order, Customer
from accounts.form import CustomerForm, OrderForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.decorators import is_user_auth, is_user_allow, is_user_admin
from django.contrib.auth.models import Group

from accounts.filters import OrderFilter


@login_required(login_url='login')
@is_user_admin
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
@is_user_allow(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    # quering child from model field
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)
    # return HttpResponse('Customer')


@login_required(login_url='login')
@is_user_allow(allowed_roles=['admin'])
def createUserCustomer(request):
    u_form = CreateUserForm()
    c_form = CustomerForm()
    if request.method == 'POST':
        u_form = CreateUserForm(request.POST)
        c_form = CustomerForm(request.POST)
        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            username = u_form.cleaned_data.get("username")
            messages.success(
                request, f'A New User:[{username}] has been created!')
            return redirect('home')
    context = {'u_form': u_form, 'c_form': c_form}
    return render(request, 'accounts/create_user_customer.html', context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', context={'products': products})
    # return HttpResponse('Products')


@login_required(login_url='login')
@is_user_allow(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': ['9rnCKPAkIOMlFTn8rJzDhZE495P2b5MfRrb5DyLfxEjvPtL9z5amMA4ZokCtJIUp'],
        #              'customer': ['2'],
        #              'product': ['3'],
        #              'status': ['Delivered'],
        #               'Submit': ['Submit']}>
        formset = OrderFormSet(request.POST, instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['admin'])
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
@is_user_allow(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@is_user_auth
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            '''
            What we want to do now?
               Take out this logic and allow our 
               signals to handle all that;

            How?
               By removing group and customer creation logics
               and allow our signals.py to handle automatically all that
               internally :)
            '''

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # # Added username because of error returning customer name if not added
            # Customer.objects.create(user=user, name=user.username,)

            messages.success(
                request, 'Account created successfully for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@is_user_auth
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
@is_user_allow(allowed_roles=['customer', 'admin'])
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
@is_user_allow(allowed_roles=['admin'])
def accountAdmin(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders)

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)
