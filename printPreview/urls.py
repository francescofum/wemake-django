from django.urls import path,include
from . import views


urlpatterns = [
    
    path('',views.print_preview,name='print_preview'),
    path('upload/',views.upload,name='print_preview'),
    
]