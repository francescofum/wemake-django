from django.db import models

from core.models import GLOBAL_MATERIALS
from core.models import GLOBAL_COLOURS
from vendor.models import Vendor


class Material(models.Model):

    '''
        A class representing a material and colour combinaiton.
        1. To query from a first get the printer object p1 = printer.objects.get(printer_id)
        then you can query the materials by calling p1.materials.all() or any other 
        function.
        2. To query based on the property of a foreign key:
        p1 = printer.objects.get(printer_id)
        p1.materials.filter(colour__name__contains="BLUE") This will return anything that contains "BLUE"
        user p1.materials.filter(name__name__iexact="ABS") if you want the exact value.
    '''

   
    # Foreign keys to relate to global material and colour tables.
    global_material = models.ForeignKey(GLOBAL_MATERIALS, related_name='material',blank=False,null=False, on_delete=models.DO_NOTHING) # On delete no cascade?    
    # Materials
    price_length      = models.DecimalField(max_digits=3, decimal_places=2,default=1.0)
    printers = models.ManyToManyField(to='printer.Printer',related_name="materials",blank=True)
    vendor = models.ForeignKey(Vendor,related_name='materials',on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['global_material', 'vendor']
        
    def __str__(self):
        return f"{self.vendor.created_by.username} {self.global_material.name}"

class Colour(models.Model):
    
    stock = models.BooleanField(default=False)
    owned_by = models.ForeignKey(Material, related_name='colours',on_delete=models.CASCADE) # On delete no cascade?
    global_colours = models.ForeignKey(GLOBAL_COLOURS, related_name='colour_global',on_delete=models.DO_NOTHING) # On delete no cascade?
    price_coefficient = models.DecimalField(max_digits=3,decimal_places=2,default=1.0)
    discount      = models.DecimalField(max_digits=3, decimal_places=2,default=1.0)

    
    class Meta:
        '''
            Custom constraing, applies SQL UNIQUE to the combination of name and material. 
            A vendor should not have two of the same material colours. e.g two RED PLA. 
        '''
        unique_together = ['global_colours', 'owned_by']
        verbose_name = 'Colour'
        verbose_name_plural = 'Colours'


    def __str__(self):
        return f"{self.owned_by.vendor.created_by.username} {self.owned_by} {self.global_colours.name}"
    
    