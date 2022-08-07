from django.urls import path 


from . import views 
from cart.views import stripe_webhook

urlpatterns = [
    path('',views.frontpage,name='frontpage'),
    path('checkout/',views.checkout,name='checkout'),
    path('success/',views.checkout_success,name='checkout_success'),
    path('webhooks/stripe/',stripe_webhook,name='stripe-webhok')

]