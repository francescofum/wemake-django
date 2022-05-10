from django.urls import path,include
from . import views

# urlpatterns = [
    # path('checkout/',views.checkout,name='checkout')

urlpatterns = [
    path('<int:id>/',views.checkout_details,name='order'),
    path('checkout/',views.checkout_details,name='order'),
    path('success/',views.success,name='success'),
]