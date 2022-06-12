from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import stripe
from django.conf import settings
from django.http import JsonResponse
from cart.cart import Cart
from vendor.models import Vendor
from order.models import Order
from order.models import OrderItem
from cart.cart import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(View):

    # Helper function to create list items from cart
    def create_list_items(self, cart):
        # result items dict
        items = []
        for product_id, data in cart.cart.items():
            items.append({
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name':
                        data['pretty_name'],
                        'description':
                        f"{data['material']} {data['colour']}",
                        # TODO: Add images 
                        # 'images': [
                        #     'https://www.bbva.ch/wp-content/uploads/2021/10/17-.-Ventajas-y-desventajas-de-la-impresion-3D-1024x493.png',
                        # ],
                        # Data to be added to OrderItem to be put here.
                        'metadata': {
                            'order_item_id': product_id
                        }
                    },
                    'unit_amount': int(float(data['price'])*100),
                },
                'quantity': data['quantity'],
            })

        return items

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        # Get the hostname
        hostname = request._current_scheme_host
        # Get the cart obj
        cart = Cart(request)

        # create_list_items 
        items = self.create_list_items(cart)
     
        # Get the venodr obj
        vendor_slug = self.kwargs['slug']
        vendor = Vendor.objects.get(slug=vendor_slug)

        # Create the Order obj, this will only have:
        # - id
        # - created_at fields.
        # This represents a checkout that hasn't gone through yet.
        # When the customer pays all the other details with be filled in.
        order = Order.objects.create(vendor=vendor)

        # Add all items to the OrderItem table
        # TODO: turn this into an iterator
        for product_id, data in cart.cart.items():
            print(product_id)
            OrderItem.objects.create(order=order,
                                     quantity=data['quantity'],
                                     price=data['price'],
                                     pretty_name=data['pretty_name'],
                                     material=data['material'],
                                     colour=data['colour'],
                                     dim_x=float(data['dims']['x']),
                                     dim_y=float(data['dims']['x']),
                                     dim_z=float(data['dims']['x']),
                                     infill=float("100"),
                                     url=data['url'])

        session = stripe.checkout.Session.create(
            # Order Metadata
            metadata={
                'vendor_id': '1',
                'order_id': order.id
            },
            # Order Items
            line_items=items,
            # Shipping
            shipping_address_collection={
                'allowed_countries': ['GB'],
            },
            shipping_options=[
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                            'amount': 0,
                            'currency': 'gbp',
                        },
                        'display_name': 'Free shipping',
                        # Delivers between 5-7 business days
                        'delivery_estimate': {
                            'minimum': {
                                'unit': 'business_day',
                                'value': 5,
                            },
                            'maximum': {
                                'unit': 'business_day',
                                'value': 7,
                            },
                        }
                    }
                },
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                            'amount': 1500,
                            'currency': 'gbp',
                        },
                        'display_name': 'Next day air',
                        # Delivers in exactly 1 business day
                        'delivery_estimate': {
                            'minimum': {
                                'unit': 'business_day',
                                'value': 1,
                            },
                            'maximum': {
                                'unit': 'business_day',
                                'value': 1,
                            },
                        }
                    }
                },
            ],
            mode='payment',
            success_url=
            f'{hostname}/success?session_id='+'{CHECKOUT_SESSION_ID}',
            cancel_url=f'{hostname}/print/{vendor_slug}'
        )

        
        return JsonResponse({'url': session.url})

