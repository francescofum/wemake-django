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
    form = VendorSettingsForm(request.POST or None, instance=vendor)
    context = {
        'form':form,
        'vendor':vendor,
        'r':request
    }
    
    print(vendor)
    if(request.method == 'GET'):
        return render(request,'vendor/vendor_admin.html',context)

    if(request.method == 'POST'):
        print(request.POST)

        if(request.POST.get('update') == '1') & form.is_valid():
            print("***********************************")
            vendor.store_name   = request.POST.get('store_name')
            vendor.slug         = request.POST.get('slug')
            vendor.description  = request.POST.get('description')
            vendor.save()


        return render(request,'vendor/vendor_admin.html',context)
