from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def is_user_auth(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def is_user_allow(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # print('Working...', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page :/")
        return wrapper_func
    return decorator


def is_user_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func
