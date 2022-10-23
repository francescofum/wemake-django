from django.contrib.auth import views as auth_views
from django.urls import path 

from . import views

urlpatterns = [
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',views.vendor_login,name='vendor_login'),
    path('vendor_admin/',views.vendor_admin,name='vendor_admin'),
    path('vendor_admin_store_gallery/',views.vendor_admin,name='vendor_admin_store_gallery'),
    path('faq/',views.faq,name='faq'),
]