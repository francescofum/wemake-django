from django.urls import path,include
from . import views

# urlpatterns = [
    # path('checkout/',views.checkout,name='checkout')

urlpatterns = [
    path('<int:id>/',views.order_details,name='order'),
    path('checkout/',views.order_details,name='order'),
    path('success/',views.success,name='success'),
]
