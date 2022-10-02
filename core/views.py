from django.shortcuts import render
import requests
import stripe
from order.models import Order, OrderItem
from vendor.models import Vendor
from cart.cart import Cart
from order.utilities import notify_vendor, notify_customer_confirmed


def frontpage(request):
    return render(request, 'core/frontpage.html')


def checkout(request):
    return render(request, 'core/checkout.html')


def checkout_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    #TODO Add shipping type
    # Get the details for the Order table
    # Amount in cents
    
    vendor_id = session.metadata['vendor_id']
    order_id  = session.metadata['order_id']
    name = session.shipping.name
    email = session.customer_details.email
    subtotal = session.amount_subtotal  # total without shipping
    country = session.shipping_address_collection.allowed_countries
    city = session.shipping.address['city']
    country = session.shipping.address['country']
    addr_ln_1 = session.shipping.address['line1']
    addr_ln_2 = session.shipping.address['line2']
    zipcode = session.shipping.address['postal_code']
    shipping_cost = session.total_details.amount_shipping
    state = session.shipping.address['state']
    # Query the shipping rate
    selected_shipping_rate = stripe.ShippingRate.retrieve(session.shipping_rate)
    # Get the display name #TODO standardise them 
    selected_shipping = selected_shipping_rate.display_name
    # total_cost = session.amount_total # Including shipping
    #TODO notes... haven't found a way to do them.    
    # FYI session.customer_details contains the address as well.

    # Retrieve the Order obj that was created earlier
    # and update it. 
    order_update_result = Order.objects.filter(pk=order_id).update(first_name=name, last_name="", email=email, address=addr_ln_1,
                                 address2=addr_ln_2,zipcode=zipcode,country=country,city=city,price_total=subtotal,price_shipping=shipping_cost,shipping_type=selected_shipping)

    if order_update_result: 
        order = Order.objects.get(pk=order_id)

        context = {
            'order' : order
        }

        cart = Cart(request)
        cart.clear()

        notify_customer_confirmed(order)
        notify_vendor(order)

    return render(request, 'core/checkout_success.html', context)
