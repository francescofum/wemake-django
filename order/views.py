import stripe

from django.conf import settings 
from django.contrib import messages
from django.shortcuts import redirect, render

from django.db.models import Q

from materials.models import Material
from materials.models import Colour

from .models import Order
from vendor.models import Vendor
from .forms import orderForm
from cart.cart import Cart 
from order.utilities import checkout

from django.core.mail import send_mail


def order_details(request,id:int=None): 
    '''
        @brief Renders a order form. The order form
        allows the user to either add  new order or 
        update an existing one depending on the value of
        'id'. 
        @param[id] The id of a order, defaults to 'None' which
        means a new order.
    '''

    cart = Cart(request)

    # # Something like this?? from the Cart @Francesco?
    # product = request.cart.product
    # vendor = request.cart.vendor??? 
    # vendor = request.user.vendor 

    # POST means we're either adding a order, 
    # updating a order or deleting one. 
    # If an id has been specified then we are editing one.
    if request.method == 'POST':
        form = orderForm(request.POST)

        if form.is_valid():
            # TODO: Enable editing order once created 
            # stripe.api_key = settings.STRIPE_SECRET.KEY
            
            # stripe_token = form.cleaned_data['stripe_token']

            # charge = stripe.Charge.create(
            #     amount = 12,
            #     currency = 'GBP',
            #     description= 'WeMake 3D Printing', 
            #     source = stripe_token
            # )
            

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']

            order = checkout(request, first_name, last_name, email, address, zipcode)

            
            # row = len(cart.cart.items()[0])
            # IF the cart array is 1D, then don't need to loop through each item
            # if row == 1:
            # text = [ 'Name:' , cart.cart.items().pretty_name , '\n' ] 
            # separator = ' '
            # email_text = separator.join(text)
            # else: 
            for key, value in cart.cart.items():
                vendor_id = value['vendor_id']
                print(value)
                text=[ 'Name:' , value['pretty_name'] , '\n' ]
                text+=[ 'Material:' , value['material'] , '\n' ]
                text+=[ 'Colour:' , value['colour'] , '\n' ]
                text+=[ 'Infill:' , str(value['infill']) , '\n' ]
                text+=[ 'Quantity:' , str(value['quantity']) , '\n' ]
                text+=[ 'Time to print (estimated):' , str(value['time_to_print']) , '\n' ]
                text+=[ 'Length of filament (estimated):' , str(value['length_of_filament']) , '\n' ]
                text+=[ 'Price:' , str(value['price']) , '\n \n \n' ]
                separator = ' '
                print(text)
                email_text = separator.join(text)

            print(email_text)

            vendor = Vendor.objects.get(id=vendor_id)
            # Send email to Vendor
            send_mail(
                'WeMake Sale!',
                "Hi, you've got a new order: \n"+email_text,
                'make.it.ffra@gmail.com',
                [vendor.email],
            )

            # Send email to Customer
            send_mail(
                'Thank you for your order!',
                "Hi, you've placed the order: \n"+email_text,
                'make.it.ffra@gmail.com',
                [email],
            )            

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
    context = {
        'form':form,
        'cart':cart.cart.items(), 
        }
    return render(request,'order/order_form.html',context)


def success(request):
    return render(request,'order/success.html')
