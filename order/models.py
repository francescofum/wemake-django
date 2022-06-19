#TODO: add thumbnail to order. https://www.youtube.com/watch?v=FN3EfKC2i6M&t=2817s
#TODO: orderMaterial class. 
# from io import BytesIO
# from PIL import Image 

from faulthandler import disable
from django.db import models
from materials.models import Material, Colour

from vendor.models import Vendor 
from core.models import GLOBAL_MATERIALS, GLOBAL_COLOURS

class Order(models.Model):
    '''
        A class representing a order. 

        How to get all the orders of a given vendor. 
        v = Vendor.objects.first() ; Get the vendor somehow
        p = v.orders.first()     ; Get the order 
        - Then you can do a few queries, let's say you want to get all the materials with the colour blue 
        p.materials.filter(colour__name__iexact="BLUE")
        -  Or all the materials... 
        p.materials.all()
    '''
    STATUS_CHOICES = (
        ('PEND', "Pending"),        # Customer hasn't payed yet
        ('CONF', "Confirmed"),      # Your order has been confirmed
        ('PRINT', "Printing"),      # STL is currently printing...
        ('DISP', "Dispatched"),     # Is on it's way
        ('DELIV', "Delivered"),     # Has been delivered. How was your delivery? 
    )

    VENDOR_PAID_CHOICES = (
        ('NO', "Unpaid"),
        ('REQ', "Requested"),
        ('CMPLT', "Complete"),
    )

    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    address2 = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    zipcode = models.CharField(max_length=255,null=True,blank=True)

    status = models.CharField(choices=STATUS_CHOICES,max_length=50,default='PEND')
    vendor_paid = models.CharField(choices=STATUS_CHOICES,max_length=50,default='NO')
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(Vendor, related_name='orders', on_delete=models.CASCADE)
    
    note = models.TextField(blank=True, null=True)
    # price fields
    price_total = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    price_shipping = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    shipping_type = models.CharField(max_length=255,null=True,blank=True) # Make these options when we have them completely defined.
                                                                          # Currently not used. 
    class Meta: 
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    pretty_name = models.TextField(blank=True, null=True)
    material = models.CharField(max_length=255)
    colour = models.CharField(max_length=255)


    infill = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    url = models.CharField(max_length=255)

    dim_x = models.DecimalField(max_digits=6, decimal_places=0)
    dim_y = models.DecimalField(max_digits=6, decimal_places=0)
    dim_z = models.DecimalField(max_digits=6, decimal_places=0)

    '''
    TODO: 
        Additional settings the customer can select:
        - Infill 
        - Finishing
        
    '''


    def __str__(self):
        return '%s' % self.id
