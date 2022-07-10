from django.conf import settings
import smtplib
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from cart.cart import Cart 

from .models import Order, OrderItem, Vendor

def checkout(request, first_name, last_name, email, address, zipcode, note, price_total):

    cart = Cart(request)
    for key, value in cart.cart.items():
        vendor = Vendor.objects.get(id=value['vendor_id'])
        break

    order = Order.objects.create(vendor= vendor, first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, note=note, price_total=price_total)


    for key, value in cart.cart.items():

        OrderItem.objects.create(order=order, quantity=value['quantity'], price=value['price'], pretty_name=value['pretty_name'], material=value['material'], colour=value['colour'], dim_x=float(value['dims']['x']), dim_y=float(value['dims']['y']), dim_z=float(value['dims']['z']), infill=float(value['infill']),  url=value['url']) #, time_to_print=float(value['time_to_print']), length_of_filament=float(value['length_of_filament']) )

    return order

def notify_vendor(order):
    from_email = settings.EMAIL_HOST_USER
    to_email = order.vendor.created_by.email

    subject = 'New Order'
    text_content = 'You have a new order'
    html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': order.vendor})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def notify_customer_confirmed(order):
    from_email = settings.EMAIL_HOST_USER

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer_recieved.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def notify_customer_payment_failed(email):
    from_email = settings.EMAIL_HOST_USER

    to_email = email
    subject = 'Order payment faled'
    text_content = 'Your order has not gone through as the payment was rejected.\nPlease try again.'
    html_content = render_to_string('order/email_notify_customer_inprogress.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def notify_customer_printing(order):
    from_email = settings.EMAIL_HOST_USER

    to_email = order.email
    subject = 'Printing..'
    text_content = 'Your STLs are printing!'
    html_content = render_to_string('order/email_notify_customer_inprogress.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def notify_customer_dispatched(order):
    from_email = settings.EMAIL_HOST_USER

    to_email = order.email
    subject = 'Order Dispatched'
    text_content = 'Your order is on its way'
    html_content = render_to_string('order/email_notify_customer_shipped.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def notify_customer_delivered(order):
    from_email = settings.EMAIL_HOST_USER

    to_email = order.email
    subject = 'Delivered'
    text_content = 'Your order has been delivered. '
    html_content = render_to_string('order/email_notify_customer_scheduled.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

