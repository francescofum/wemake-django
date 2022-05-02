from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from cart.cart import Cart 

from .models import Order, OrderItem
from vendor.models import Vendor

def checkout(request, first_name, last_name, email, address, zipcode):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode)

    cart = Cart(request)

    for key, value in cart.cart.items():
        vendor = Vendor.objects.get(id=value['vendor_id'])

        print(float(value['dims']['x']))
        OrderItem.objects.create(order=order, vendor=vendor, quantity=value['quantity'], price=value['price'], pretty_name=value['pretty_name'], material=value['material'], colour=value['colour'], dim_x=float(value['dims']['x']), dim_y=float(value['dims']['y']), dim_z=float(value['dims']['z']), infill=float(value['infill'])) #, time_to_print=float(value['time_to_print']), length_of_filament=float(value['length_of_filament']) )
        order.vendors.add(value['vendor_id'])

    return order

def notify_vendor(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for vendor in order.vendors.all():
        to_email = vendor.created_by.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': vendor})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()