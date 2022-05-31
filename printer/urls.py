from django.urls import path,include
from . import views
# from .forms import PrinterForm

urlpatterns = [
    path('<int:id>/slicer_check/upload_vendor/',views.upload_vendor,name='upload_stl_vendor'),
    path('<int:id>/',views.printer_details,name='printer'),
    path('',views.printer_details,name='printer'),
    path('printer_dashboard/',views.printer_dashboard,name='printer_dashboard'), 
    path('<int:id>/slicer_check/',views.slicer_check,name='slicer_check'),
    path('<int:id>/slicer_check/get_available_printers_vendor/',views.get_available_printers_vendor,name='get_available_printers_vendor'),
]