from django.shortcuts import render, redirect

# Create your views here.

# def checkout(request):
#     '''
#         Main entry point for checkout
#     '''

#     if(request.method == 'GET'):
#         context = {
#             # 'vendor':vendor,
#             # 'printers':printers
#         }        
#         return render(request,'checkout.html', context)

from django.db.models import Q

from materials.models import Material
from materials.models import Colour

from .models import Order
from vendor.models import Vendor
from .forms import orderForm

from cart.cart import Cart 

from utilities import checkout

def order_details(request,id:int=None): 
    '''
        @brief Renders a order form. The order form
        allows the user to either add  new order or 
        update an existing one depending on the value of
        'id'. 
        @param[id] The id of a order, defaults to 'None' which
        means a new order.
    '''

    # # Something like this?? from the Cart @Francesco?
    # product = request.cart.product
    # vendor = request.cart.vendor??? 
    # vendor = request.user.vendor 

    # POST means we're either adding a order, 
    # updating a order or deleting one. 
    # If an id has been specified then we are editing one.
    if request.method == 'POST':
        form = orderForm(request.POST)

        cart = Cart(request)

        if form.is_valid():
            # TODO: 
            # Stripe
            # Enable editing order once created 

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            note = form.cleaned_data['note']

            order = checkout(request, first_name, last_name, email, address, zipcode, note)

            cart.clear()

            return redirect('success')

        else:
            # TODO: Handle not valid form.
            print("NOT OK")

    # Either display an existing order,
    # or a blank form for a new order.
    if request.method == "GET":
        # if id is not None:
        #     order = order.objects.get(pk=id)
        #     form = orderForm(instance = order,prefix="order")
        #     material_form = MaterialForm(vendor=vendor,order=order,prefix="material")
        # else:
        form = orderForm()

    # Render the form 
    context = {'form':form}
    return render(request,'order/order_form.html',context)


