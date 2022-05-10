from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import VendorSettingsForm
from .models import Vendor 
from order.views import checkout_details
from order.forms import orderForm, orderForm_Vendor
from order.models import Order
from order.utilities import notify_customer

@login_required
def vendor_admin(request):
    '''
        Main entry point for vendor (dashboards/orders etc)
    '''

    vendor = request.user.vendor
    
    if(request.method == 'GET'):
        form = VendorSettingsForm(instance=vendor)
        context = {
            'form':form,
            'vendor':vendor,
        }        
        return render(request,'vendor/vendor_admin.html',context)

    if(request.method == 'POST'):
        form = VendorSettingsForm(request.POST, request.FILES, instance=vendor)
        context = {
            'form':form,
            'vendor':vendor,
        }        

        if (form.is_valid()):
            form.save()
            vendor.store_logo_thumbnail = '' # Ensures thumbnail is re-loaded when new pic is uploaded (can be optimised tho)

        return redirect('vendor_home')


@login_required
def vendor_home(request):
    '''
        Main entry point for vendor home
    '''

    vendor = request.user.vendor
    if request.method == 'GET':

        for key in vendor.orders.all() : 
            order = Order.objects.get(pk=key.id)
            form = orderForm_Vendor(request.GET, instance = order)
            FIELD_NAMES = ['price_total',  'slug', 'address', 'address2', 'city', 'country', 'zipcode' , 'email', 'first_name', 'last_name', 'note',  ] 
            for field in FIELD_NAMES: 
                form.fields[field].disabled = True
                
            # form = VendorSettingsForm(instance=vendor)

    if request.method == 'POST':

        for key in vendor.orders.all() : 
            order = Order.objects.get(pk=key.id)
            form = orderForm_Vendor(request.POST, instance = order)
            FIELD_NAMES = ['price_total',  'slug', 'address', 'address2', 'city', 'country', 'zipcode' , 'email', 'first_name', 'last_name', 'note',  ] 
            for field in FIELD_NAMES: 
                form.fields[field].disabled = True



        form.save()
        if form.is_valid():
            print('notify customer')


    context = {
        'form':form,
        'vendor':vendor
        }      

    return render(request,'vendor/vendor_home.html',context)


