from django.urls import path 


from . import views 

urlpatterns = [
    path('',views.frontpage,name='frontpage'),
    path('checkout/',views.checkout,name='checkout'),
    path('success/',views.checkout_success,name='checkout_success'),
    

]