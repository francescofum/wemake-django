import os

from django.shortcuts import render
from django.http import JsonResponse

from vendor.models import Vendor
from .models import STL

def print_preview(request):
    vendor = Vendor.objects.first()
    context = {'vendor':vendor}
    x = vendor.get_unique_materials()
    return render(request,'print_preview/print_preview.html',context)

def upload(request):
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        title = file.name
        stl = STL(file=file,pretty_name=title)
        stl.save()
    
    response = {
        'id': stl.id,
        'url':stl.file.url,
        'pretty_name': stl.pretty_name,
    }
    return JsonResponse(response,status=200)

