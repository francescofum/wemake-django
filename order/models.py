#TODO: add thumbnail to order. https://www.youtube.com/watch?v=FN3EfKC2i6M&t=2817s
#TODO: orderMaterial class. 
# from io import BytesIO
# from PIL import Image 

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
    first_name = models.CharField(max_length=255,blank=False,null=False)
    last_name = models.CharField(max_length=255,blank=False,null=False)
    email = models.CharField(max_length=255,blank=False,null=False)
    address = models.CharField(max_length=255,blank=False,null=False)
    address2 = models.CharField(max_length=255,blank=False,null=False)
    country = models.CharField(max_length=255,blank=False,null=False)
    city = models.CharField(max_length=255,blank=False,null=False)
    zipcode = models.CharField(max_length=255,blank=False,null=False)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    note = models.TextField(blank=True, null=True)
    # price fields
    price_total = models.DecimalField(max_digits=6, decimal_places=2)


    class Meta: 
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order= models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='orders', on_delete=models.CASCADE)
    vendor_has_been_paid = models.BooleanField(default=False)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    name = models.TextField(blank=True, null=True)
    material = models.ForeignKey(Material, related_name='materials', on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, related_name='colour', on_delete=models.CASCADE)



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
