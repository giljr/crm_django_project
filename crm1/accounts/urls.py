from accounts import views
from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('create_customer/', views.createUserCustomer,
         name="create_user_customer"),
    path('products/', views.products, name="products"),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('user_page/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name='account'),
    path('account_admin/<str:pk>/', views.accountAdmin, name='account_admin'),
    path('password_reset/', auth_view.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html'
    ),
        name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ),
        name='password_reset_confirm'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ),
        name='password_reset_done'),
    path('password_reset/complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ),
        name='password_reset_complete'),
]


'''
1 - Forgot pw?        , password_reset_form   , //PasswordResetView.as_view()         , [Submit email form]
2 - link rst form     , password_reset_confirm, //PasswordResetConfirmView.as_view()  , [Enter email now! link to reset in email]
3 - email sent!       , password_reset_done   , //PasswordResetDoneView.as_view()     , [Email sent!]
4 - password changed! ,password_reset_complete, //PasswordResetCompleteView.as_view(), [Password successfully Changed!] 
'''
