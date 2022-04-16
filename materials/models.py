from django.db import models

from core.models import MATERIAL_GLOBAL
from core.models import COLOUR_GLOBAL
from vendor.models import Vendor


class MaterialOptions(models.Model):

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

    # Quantity in kg of the material.
    #quantity = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    quantity = models.BooleanField(default=True)
    # Price coefficient  as a % 
    price_coefficient = models.DecimalField(max_digits=3,decimal_places=2,default=1.0)
    price_length      = models.DecimalField(max_digits=3, decimal_places=2,default=1.0)
    # Foreign keys to relate to global material and colour tables.
    material = models.ForeignKey(MATERIAL_GLOBAL, related_name='material',on_delete=models.DO_NOTHING) # On delete no cascade?
    colour   = models.ForeignKey(COLOUR_GLOBAL, related_name='colour',on_delete=models.DO_NOTHING) # On delete no cascade?

    # Materials
    printers = models.ManyToManyField(to='printer.Printer',related_name="materials")
    vendor = models.ForeignKey(Vendor,related_name='materials',on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.material.name} {self.colour.name}"
