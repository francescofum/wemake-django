import json
import os

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
   
        
        # stl_name = request.POST.get('name')
        # material = request.POST.get('material')
        # colour = request.POST.get('colour')
        # if (stl_name is None or material == "Select" or colour == "Select"):
        #     return JsonResponse(response,status=200) 
        # dims={}
        # dims['x'] = float(request.POST.get('size_x'))
        # dims['y'] = float(request.POST.get('size_y'))
        # dims['z'] = float(request.POST.get('size_z'))

        # vendor = Vendor.objects.get(slug=slug)
        # compatible_printers = vendor.get_compatible_printers(material,colour,dims)
        # response = {'printers':compatible_printers}
    return JsonResponse(response,status=200)

# This is old, stripe handles that now. 
# def add_to_cart(request,slug):
#     response = {}
#     stl_list = request.POST.get('stl_list')
#     stl_list = json.loads(stl_list)

#     cart = Cart(request)
#     vendor = Vendor.objects.get(slug=slug)
    
#     for id in stl_list:
#         stl_list[id]['vendor_id'] = vendor.id # should be added to stl_list directly, long term
#         cart.add(stl_list[id]['id'], data=stl_list[id], update_quantity=False)

#     print(cart.cart)
#     return JsonResponse(response,status=200)

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
