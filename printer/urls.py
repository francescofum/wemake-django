from django.urls import path,include
from . import views
# from .forms import PrinterForm

urlpatterns = [
    path('<slug:slug>/upload/',views.upload,name='upload_stl'),
    path('<int:id>/',views.printer_details,name='printer'),
    path('',views.printer_details,name='printer'),
    path('printer_dashboard/',views.printer_dashboard,name='printer_dashboard'), 
    path('slicer_check/',views.slicer_check,name='slicer_check'),
    path('<slug:slug>/get_available_printers/',views.get_available_printers,name='get_available_printers'),
]