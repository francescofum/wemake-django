from django.urls import path 


from . import views 
from cart.views import stripe_webhook

urlpatterns = [
    path('',views.frontpage_main,name='frontpage_main'),
    path('vendor-info/',views.frontpage_vendors,name='frontpage_vendors'),
    path('checkout/',views.checkout,name='checkout'),
    path('success/',views.checkout_success,name='checkout_success'),
    path('webhooks/stripe/',stripe_webhook,name='stripe-webhok')

]