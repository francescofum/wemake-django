from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .forms import VendorSettingsForm
from .models import Vendor 


@login_required
def vendor_admin(request):
    '''
        Main entry point for vendor (dashboards/orders etc)
    '''

    vendor = request.user.vendor
    print("***********************************")
    print(request.method)

    if(request.method == 'GET'):
        form = VendorSettingsForm(None, instance=vendor)
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
            context = {
                'form':form,
                'vendor':vendor,
            }        
        return render(request,'vendor/vendor_admin.html',context)


