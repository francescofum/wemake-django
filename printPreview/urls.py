from django.urls import path,include
from . import views
from cart.views import CreateCheckoutSession, stripe_webhook


urlpatterns = [
    
    path('<slug:slug>/',views.print_preview,name='print_preview'),
    path('<slug:slug>/upload/',views.upload,name='upload_stl'),
    path('<slug:slug>/add_to_cart/',CreateCheckoutSession.as_view(),name='add_to_cart'),
    path('<slug:slug>/remove_item_from_cart/',views.remove_from_cart,name='remove_from_cart'),
    path('<slug:slug>/get_available_printers/',views.get_available_printers,name='get_available_printers'),
    path('<slug:slug>/send_vendor_query/',views.send_vendor_query,name='send_vendor_query'),
    
]