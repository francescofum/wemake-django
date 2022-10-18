import json
import os
import re

from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from vendor.models import Vendor
from cart.cart import Cart 

from .models import STL
from order.views import checkout_details

def print_preview(request,slug):
    materials = {}
    # vendor = Vendor.objects.filter(slug=slug)
    vendor = get_object_or_404(Vendor,slug=slug)
    materials_json = vendor.serialize_materials_for_print_preview()
    print('materials_json:')
    print(materials_json)
    
    # Clear the cart
    # TODO: repopulate the table w/ cart items
    cart = Cart(request)
    cart.clear()

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

    cart = Cart(request)
    cart.add(stl.id,response)

    return JsonResponse(response,status=200)

def get_available_printers(request,slug):
    '''
        Gets availabe printers, this is called whenever a change is made
        to the stl row. 
        TODO: update the cart with new items. 
    '''
    if request.method == 'POST':
        response = {}

        stl_data = json.loads(request.POST.get('stl_data'))
        product_id = stl_data['id']

   
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

            stl_material_colour  = {'material':material, 'colour': colour}
            
            price = printer.quote(cura_data,stl_material_colour)
            price = "{:.2f}".format(price)

            response = {'printer_id':compatible_printers[0].id,
            'stl_id':stl_id,
            'cura_data':cura_data,
            'price':price}

            # Update the cart 
            cart = Cart(request)
            stl_data['price'] = price
            stl_data['printer'] = response['printer_id']
            stl_data['cura_data'] = response['cura_data']

            cart.update(product_id,stl_data)


        else:
            # Hanlde no compatible printers, display some error. 
            response = {'printer_id':"KO",
            'stl_id':"KO",
            'cura_data':"KO",
            'price':"KO"}
           


    

    
                    
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


def send_vendor_query(request,slug):
    from_email = settings.EMAIL_HOST_USER
    vendor = Vendor.objects.get(slug=slug)
    to_email = request.POST.get('email')
    topic = request.POST.get('topic')
    body = request.POST.get('description')
    subject = f"New message re: {topic}"

    context = {
        'from':from_email,
        'to':to_email,
        'subject':subject,
        'body':body
    }
    text_content = 'You have a new query'
    html_content = render_to_string('print_preview/contact_vendor_email.html', context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
  
    response = {} 
    return JsonResponse(response,status=200)
