from django.urls import path,include
from . import views
# from .forms import orderForm

urlpatterns = [
    path('<int:id>/',views.order_details,name='order'),
    path('checkout/',views.order_details,name='order'),
]