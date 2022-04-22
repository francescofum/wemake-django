from django.urls import path,include
from . import views
# from .forms import PrinterForm

urlpatterns = [
    path('checkout/',views.checkout,name='checkout')
]