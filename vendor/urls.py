from django.contrib.auth import views as auth_views
from django.urls import path 

from . import views

urlpatterns = [
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='vendor/login.html'),name='login'),
    path('vendor_admin/',views.vendor_admin,name='vendor_admin'),
    path('vendor_home/',views.vendor_home,name='vendor_home'),
]