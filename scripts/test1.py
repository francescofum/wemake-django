from printer.models import *
from vendor.models import * 
from django.core import serializers

from pprint import pprint as pp 
# def run():
    # vendor = Vendor.objects.get(id=1)
    # materials = vendor.get_unique_materials()
    # print(materials)
    # materials = vendor.get_material('ABS')
    # print(materials)

# Creating a printer 
def run():
    vendor = Vendor.objects.get(id=1)
    p1 = Printer.objects.create(
        name="myPrinter1",
        is_active=True,
        slug="myPrinter1",
        vendor=vendor,
        description="Programmatically adding a printer",
        price_energy = 10.01,
        price_length = 10.01,
        price_min    = 10.01,
        price_hour   = 10.01,
        price_margin = 10.01,
        tray_length = 1000,
        tray_width  = 1000,
        tray_height = 1000,
        power = 100
    )


    


 
# def run():
#     '''
#     Serialise with json
#     '''
#     vendor = Vendor.objects.get(id=1)

#     printer = vendor.printers.first()
#     materials = printer.materials.all()
#     json = serializers.serialize("json", materials)
#     pp(json)