from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import VendorSettingsForm
from .models import Vendor 
from order.views import checkout_details
from order.forms import orderForm, orderForm_Vendor
from order.models import Order
from order.utilities import notify_customer_recieved

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

        return redirect('order_dashboard')


@login_required
def faq(request):
    '''
        Vendor FAQ's page entry point
    '''

    vendor = request.user.vendor

    context = {
        'vendor':vendor
    }        
    return render(request,'vendor/faq.html',context)
