from django.urls import path,include
from . import views
# from .forms import PrinterForm

urlpatterns = [
    path('<int:id>/',views.material_details,name='material'),
    path('',views.material_details,name='material'),
    path('material_dashboard/',views.material_dashboard,name='material_dashboard')
]