from printer.models import *
from vendor.models import * 
from materials.models import *
from django.core import serializers
from django.db.models import Q

from pprint import pprint as pp 
from django.forms.models import model_to_dict

'''
    How To: python manage.py runscript snippets

'''
## Add a printer 
# def run():
#     vendor = Vendor.objects.first()
#     p1 = Printer.objects.create(
#         name="myPrinter2",
#         is_active=True,
#         slug="myPrinter2",
#         vendor=vendor,
#         description="Programmatically adding a printer",
#         price_energy = 10.01,
#         price_length = 10.01,
#         price_min    = 10.01,
#         price_hour   = 10.01,
#         price_margin = 10.01,
#         tray_length = 1000,
#         tray_width  = 1000,
#         tray_height = 1000,
#         power = 100
#     )


## Update a printer 
def run():
    # Printer
    # create_printer()
    # delete_printer()
    # # Material
    # create_material()
    # update_material()
    # assign_material_to_printer()
    # unassign_material_from_printer()
    # delete_material()
    # update_vendor_settings()

    # get_materials_with_colours()
    printers = get_compatible_printers('ABS','BLACK',size={'x':1000,'y':2000,'z':3000})
    print(10*"*")
    print(printers)
def get_compatible_printers(sel_material:str,sel_colour:str,size:dict) -> list:
    '''
        @brief: Returns a list of compatible printers based on:
                - Colour
                - Material
                - Model dimensions

        @parm[material] : The material, in string format. 
        @parm[colour]   : The colour, in string format. 
        @parm[size]     : The dimensions of the model {'x': , 'y': , 'z'}
        @return: A list of printer objects
    '''
    compatible_printers = []
    # Scale factor
    scale = 0.9

    # get the vendor 
    vendor = Vendor.objects.first()

    printers = set()
    # Get the printers which can do the material and colour
    for printer in vendor.printers.all():
        # Check if printer can handle colour and material
        
        # get all the materials 
        materials = printer.materials.all()
        # loo over each material and get the colour 
        for material in materials:
            colours = material.colours.all()
            if material.global_material.name == sel_material:
                for colour in colours:
                    if colour.global_colours.name == sel_colour:
                        # check if printer can handle model dims
                        if( (size['x'] < printer.tray_length * scale ) and 
                            (size['y'] < printer.tray_width  * scale )  and 
                            (size['z'] < printer.tray_height * scale )): 
                            compatible_printers.append(printer)

    return list(compatible_printers)


def get_materials_with_colours():
    materials_json = {}
    vendor = Vendor.objects.first()
    materials = vendor.materials.all()
    for material in materials:
        materials_json[material.global_material.id] = {}
        materials_json[material.global_material.id]['name'] = material.global_material.name
        materials_json[material.global_material.id]['colours'] = {}
        for colour in material.colours.all():
            materials_json[material.global_material.id]['colours'][colour.id] = colour.global_colours.name
    
    pp(materials_json)
            
    

def get_materials():
    vendor = Vendor.objects.first()
    mat = vendor.materials.all()
    pp(mat)

def update_vendor_settings():
    from django.test import  Client
    from django.urls import reverse

    client = Client()
    login_url = reverse('login')
    vendor_admin_url = reverse('vendor_admin')

    # Login
    response = client.post(login_url, {'username': 'francesco', 'password': 'athens123'})
    # Simulate updating the name 
    response = client.post(vendor_admin_url,\
        {'update':'1','store_name':'OldName',\
        'slug':"somenewslug",\
        'description':"Some desc"},\
        follow=True)
    
def create_printer():
    '''
        Create a printer 
    '''
    vendor = Vendor.objects.first()
    p1 = Printer.objects.create(
        name="myPrinter2",
        is_active=True,
        slug="myPrinter2",
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

def update_material():
    '''
        Updating a printer 
    '''
    # Get the vendor 
    vendor = Vendor.objects.first()
    # Get the printer 
    p1 = Printer.objects.first()
    p1.name = "HELLO!"
    p1.description = "I have a new description"
    # Remember to always save!
    p1.save()

def create_material():
    '''
        Create a material 
    '''
    # Get the vendor 
    vendor = Vendor.objects.first()
    # Get the material 
    material_global = GLOBAL_MATERIALS.objects.last()
    # Get the colour 
    colour_global   = GLOBAL_COLOURS.objects.first()
   
    # Check if the material already exists. 
    exists = Material.objects.filter(Q(colour__name__iexact=colour_global.name) &
                                            Q(material__name__iexact=material_global.name) &
                                            Q(vendor__id__iexact=vendor.id)).exists()

    if not exists:
        material1 = Material.objects.create(
                    quantity = 1,
                    price_coefficient = 1.1,
                    price_length = 1.1,
                    material = material_global,
                    colour = colour_global,
                    vendor = vendor)
        print(f"Successfully added: {material1}")
    else:
        print(f"{material_global.name} {colour_global.name} already exists")

def assign_material_to_printer():
    '''
        Assign a material to a printer 
    '''
    # Get the vendor 
    vendor = Vendor.objects.first()
    # Get the printer 
    p1 = Printer.objects.first()
    # Get the material 
    material = vendor.materials.first()
    # Assign material to printer
    material.printers.add(p1)

def unassign_material_from_printer():
    '''
        Unassign a material from a printer 
    '''
    # Get the vendor 
    vendor = Vendor.objects.first()
    # Get the printer 
    p1 = Printer.objects.first()
    # Get the material 
    material = vendor.materials.first()
    # Assign material to printer
    material.printers.remove(p1)

def delete_material():
    '''
        Delete a material 
    '''
    # Get the vendor 
    vendor = Vendor.objects.first()
    # Get the material 
    material = Material.objects.first()
    # Delete it
    material.delete()

def delete_printer():
    '''
        Delete a printer 
    '''
    # Get the vendor 
    vendor = Vendor.objects.first()
    # Get the printer 
    p1 = Printer.objects.first()
    p1.delete()
