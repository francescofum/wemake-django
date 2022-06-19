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
from django.contrib.auth.decorators import login_required

from materials.models import Material
from materials.models import Colour

from .models import Order
from vendor.models import Vendor
from .forms import orderForm, orderForm_Vendor
from order.utilities import notify_vendor, notify_customer_confirmed, notify_customer_printing, notify_customer_dispatched, notify_customer_delivered



from cart.cart import Cart 

from .utilities import checkout

def checkout_details(request,  id:int=None): 
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
            price_total = 3 

            order = checkout(request, first_name, last_name, email, address, zipcode, note, price_total)
            
            notify_vendor(order)
            
            cart.clear()

            return redirect('success')

        else:
            # TODO: Handle not valid form.
            print("NOT OK")

    # Either display an existing order,
    # or a blank form for a new order.
    if request.method == "GET":
        if id is not None:
            order = Order.objects.get(pk=id)
            form = orderForm(instance = order)
        else:
            form = orderForm()

    # Render the form 
    context = {'form':form}
    return render(request,'order/checkout_form.html',context)


def success(request):
    return render(request,'order/success.html')



@login_required
def order_details(request, id:int=None):
    '''
        Main entry point for vendor home
    '''

    vendor = request.user.vendor
    if request.method == 'GET':

        if id is not None:
            order = Order.objects.get(pk=id)
            form = orderForm_Vendor(instance = order)
        else:
            form = orderForm_Vendor()



        context = {
            'form':form,
            'vendor':vendor
            }      
        return render(request,'order/order_form.html',context)
        
    if request.method == 'POST':
        order = Order.objects.get(pk=id)
        form = orderForm_Vendor(request.POST, instance = order)

        FIELD_NAMES = ['price_total',  'address', 'address2', 'city', 'country', 'zipcode' , 'email', 'first_name', 'last_name', 'note',  ] 
        for field in FIELD_NAMES: 
            form.fields[field].disabled = True
        
        if form.is_valid():

            # Order status
            status= form.cleaned_data.get("status")
            
            if status == 'CONF': 
                notify_customer_confirmed(order)

            if status == 'PRINT': 
                notify_customer_printing(order)

            if status == 'DISP': 
                notify_customer_dispatched(order)

            if status == 'DELIV': 
                notify_customer_delivered(order)

            form.save()

            context = {
                'vendor':vendor
                }      

        else:
            print(form.errors.as_data()) 

        return redirect('order_dashboard')     # form.save
            # print('notify customer')
            # return redirect('order_dashboard')





@login_required
def order_dashboard(request):
    '''
        Main entry point for vendor (dashboards/orders etc)
    '''

    vendor = request.user.vendor

    if(request.method == 'GET'):
        context = {
            'vendor':vendor,
        }        
        return render(request,'order/order_dashboard.html',context)
