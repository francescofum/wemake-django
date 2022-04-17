from django.urls import path,include
from . import views
# from .forms import PrinterForm

urlpatterns = [
    path('<int:id>/',views.printer_details,name='printer'),
    path('',views.printer_details,name='printer'),
]