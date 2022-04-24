from django.urls import path,include
from . import views
# from .forms import PrinterForm

urlpatterns = [
    path('<int:id>/',views.material_details,name='printer'),
    path('',views.material_details,name='printer'),
]