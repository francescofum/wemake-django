#TODO: add thumbnail to printer. https://www.youtube.com/watch?v=FN3EfKC2i6M&t=2817s
#TODO: PrinterMaterial class. 
# from io import BytesIO
# from PIL import Image 

from django.db import models

from vendor.models import Vendor 
from core.models import GLOBAL_MATERIALS, GLOBAL_COLOURS
from materials.models import  Material

class Printer(models.Model):
    '''
        A class representing a printer. 

        How to get all the printers of a given vendor. 
        v = Vendor.objects.first() ; Get the vendor somehow
        p = v.printers.first()     ; Get the printer 
        - Then you can do a few queries, let's say you want to get all the materials with the colour blue 
        p.materials.filter(colour__name__iexact="BLUE")
        -  Or all the materials... 
        p.materials.all()
    '''
    name = models.CharField(max_length=255,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255)
    vendor = models.ForeignKey(Vendor, related_name='printers', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # price fields
    price_energy = models.DecimalField(max_digits=6, decimal_places=2)
    price_length = models.DecimalField(max_digits=6, decimal_places=2)
    price_min    = models.DecimalField(max_digits=6, decimal_places=2)
    price_hour   = models.DecimalField(max_digits=6, decimal_places=2)
    price_margin = models.DecimalField(max_digits=6, decimal_places=2)
    # dimensions (mm)
    tray_length = models.IntegerField()
    tray_width  = models.IntegerField()
    tray_height = models.IntegerField()
    # power (w)
    power = models.FloatField()
    # Cura config 
    config    = models.FileField(upload_to='uploads/',blank=True,null=True)
    # image     = models.ImageField(upload_to='uploads/',blank=True,null=True) #TODO
    # thumbnail = models.ImageField(upload_to='uploads/',blank=True,null=True) #TODO



    class Meta: 
        ordering = ['-date_added']

    def __str__(self):
        return self.name 

    def get_materials(self):
        printer = Printer.objects.get(pk=self.id)
        return printer.materials.all()
     
    

