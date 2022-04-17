
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Vendor 

@login_required
def vendor_admin(request):
    '''
        Main entry point for vendor (dashboards/orders etc)
    '''
    
    vendor = request.user.vendor
    
    if(request.method == 'GET'):
        return render(request,'vendor/vendor_admin.html',{'vendor':vendor})

    if(request.method == 'POST'):
        
        if(request.POST.get('update') == '1'):
            print("***********************************")
            vendor.store_name = request.POST.get('store_name')
            vendor.slug = request.POST.get('slug')
            vendor.description = request.POST.get('description')
            vendor.save()

        return render(request,'vendor/vendor_admin.html',{'vendor':vendor,'r':request})
