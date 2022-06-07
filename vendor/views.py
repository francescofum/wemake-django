from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import VendorGalleryForm, VendorSettingsForm
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
        form = VendorSettingsForm(instance=vendor,prefix="vendor_details")
        # Create a list of gallery forms 
        gallery_form_list = []
        for gallery in vendor.gallery.all():
            gallery_form_list.append(VendorGalleryForm(instance=gallery,prefix=f"gallery_form_{gallery.id}"))
        context = {
            'form':form,
            'img_form':gallery_form_list,
            'vendor':vendor,
        }      
        return render(request,'vendor/vendor_admin.html',context)

    if(request.method == 'POST'):
        vendor = request.user.vendor
        # First get the vendor details form, theen we'll get the gallery.
        form = VendorSettingsForm(request.POST,request.FILES, prefix="vendor_details",instance=vendor)
        if (form.is_valid()):
            vendor.store_logo_thumbnail = '' # Ensures thumbnail is re-loaded when new pic is uploaded (can be optimised tho)
            form.save()
        # Now get the gallery form 
        gallery_form_list = [VendorGalleryForm(request.POST,request.FILES,instance=gallery,prefix=f"gallery_form_{gallery.id}") for gallery in vendor.gallery.all()]
        # Validate and save each form 
        for form in gallery_form_list:
            if (form.is_valid()):
                gallery_item = form.save(commit=False)
                # gallery_item.vendor = vendor
                gallery_item.save()

        context = {
            'form':form,
            'img_form':gallery_form_list,
            'vendor':vendor,
        }        

        return redirect('vendor_admin')

@login_required
def vendor_admin_store_gallery(request):
    pass

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
