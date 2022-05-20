from django.urls import path,include
from . import views

# urlpatterns = [
    # path('checkout/',views.checkout,name='checkout')

urlpatterns = [
    path('checkout/',views.checkout_details,name='checkout'),
    path('success/',views.success,name='success'),
    path('order_dashboard/',views.order_dashboard,name='order_dashboard'),
    path('<int:id>/',views.order_details,name='order'),
    path('',views.order_details,name='order'),
]