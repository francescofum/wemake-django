import json
import os
import re

from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json

from vendor.models import Vendor
from cart.cart import Cart 

from .models import STL
from order.views import checkout_details

def print_preview(request,slug):
    materials = {}
    # vendor = Vendor.objects.filter(slug=slug)
    vendor = get_object_or_404(Vendor,slug=slug)
    materials_json = vendor.serialize_materials_for_print_preview()


    context = {'vendor':vendor,'materials_json':json.dumps(materials_json)}
    import pprint
    pprint.pprint(materials)
    return render(request,'print_preview/print_preview.html',context)

# AJAX CALLS

def upload(request,slug):
    '''
        Handles uploading an stl.
    '''
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        title = file.name
        stl = STL(file=file,pretty_name=title)
        try:
            stl.save()
        except Exception as e:
            print(e)
    
    response = {
        'id': stl.id,
        'filename':stl.file.name,
        'path':stl.file.path,
        'url':stl.file.url,
        'pretty_name': stl.pretty_name,
    }
    return JsonResponse(response,status=200)

def get_available_printers(request,slug):
    '''
        Gets availabe printers, this is called whenever a change is made
        to the stl row. 
        TODO: update the cart with new items. 
    '''
    if request.method == 'POST':
        response = {}
        # Update the cart 
        cart = Cart(request)
        stl_data = json.loads(request.POST.get('stl_data'))
        product_id = stl_data['id']
        cart.add(product_id,stl_data)
   
        dims={}
        stl_name = stl_data['pretty_name']
        stl_filename = "/" + stl_data['filename']
        stl_id = stl_data['id']
        material = stl_data['material']
        colour = stl_data['colour']
        if (stl_name is None or material == "Select" or colour == "Select"):
            return JsonResponse(response,status=200) 
        dims['x'] = float(stl_data['dims']['x'])
        dims['y'] = float(stl_data['dims']['y'])
        dims['z'] = float(stl_data['dims']['z'])

        vendor = Vendor.objects.get(slug=slug)
        compatible_printers = vendor.get_compatible_printers(material,colour,dims)
        
        if len(compatible_printers) > 0:
            # select the first TODO: select the cheapest
            printer = compatible_printers[0]
            cura_data = printer.slice(stl_filename)

            stl_data  = {'material':material, 'colour': colour}
            
            price = printer.quote(cura_data,stl_data)
            price = "{:.2f}".format(price)
        else:
            # Hanlde no compatible printers, display some error. 
            pass
           

        response = {'printer_id':compatible_printers[0].id,
                    'stl_id':stl_id,
                    'cura_data':cura_data,
                    'price':price}
                    
    return JsonResponse(response,status=200,safe=False)

def remove_from_cart(request,slug,):
    response = {}
    stl_id = request.POST.get('stl_id')
 

    cart = Cart(request)
    cart.remove(stl_id)

    return JsonResponse(response,status=200)


def go_to_checkout(request):
    response = {} 

    cart = Cart(request)
    
    checkout_details(request,cart)

    return JsonResponse(response,status=500) # only arrives here if error
