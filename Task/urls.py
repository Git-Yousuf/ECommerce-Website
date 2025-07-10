"""
URL configuration for Task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from adm import views
from Task import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('LoginSignup', views.LoginSignup, name='LoginSignup'),
    path("Logout", views.Logout, name="Logout"),
    path('Cart', views.CartPage, name='Cart'),
    path('AllItems', views.AllItems, name='AllItems'),
    path('ForgetPassword', views.ForgetPassword, name='ForgetPassword'),
    path('Register', views.Register, name='Register'),
    path('OTPValidation', views.OTPValidation, name='OTPValidation'),
    path('ResetPassword', views.ResetPassword, name='ResetPassword'),
    path('ItemDetailsView', views.ItemDetailsView, name='ItemDetailsView'),
    path('AddItem', views.AddItem, name='AddItem'),
    path('AdminLogin', views.AdminLogin, name='AdminLogin'),
    path('DeleteItem/<pk>', views.DeleteItem, name='DeleteItem'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('UserDetailsView', views.UserDetailsView, name='UserDetailsView'),
    path('DeleteUser/<int:user_id>/', views.DeleteUser, name='DeleteUser'),
    path('add_to_cart/<int:item_code>/', views.add_to_cart, name='add_to_cart'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('ProceedCart', views.ProceedCart, name='ProceedCart'),
    path('PurchaseConfirmation', views.PurchaseConfirmation, name='PurchaseConfirmation'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
