#TODO: add thumbnail to printer. https://www.youtube.com/watch?v=FN3EfKC2i6M&t=2817s
#TODO: PrinterMaterial class. 
# from io import BytesIO
# from PIL import Image 

from django.db import models

from vendor.models import Vendor 
from core.models import GLOBAL_MATERIALS, GLOBAL_COLOURS
from materials.models import  Material
import json
import requests

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
    price_length = models.DecimalField(max_digits=6, decimal_places=2) #TODO we have a price lenght in material. 
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
    
    def slice(self,stl_id):
        # TODO: put wm_slicer_cura in the env, don't hardcode.
        # TOOD: put port in env, don't hardcode.
        response = requests.post('http://wm_slicer_cura:5555/analyse_stl', json={"stl_id": stl_id,'printe_id':self.id})
    
        if response.status_code == 200:
            data = json.loads(response.text)
            # TODO: response should be a dictionary of numbers, 
            # not a dictionary of lists with one element.
            # Indexing a 1-element list looks bad and is confusing.
            data['fil_len'] = float(data['fil_len'])
            data['fil_vol'] = int(data['fil_vol'])
            data['print_s'] = int(data['print_s'])
            data['print_hms'] = data['print_hms']

            return data


        

    def quote(self,cura_data,stl_data):
        #TODO Decide where we want price_length to be.
        # In the material? or in the printer? or both? 
        printer = Printer.objects.get(pk=self.id)
        
        # TODO This is done in two steps, do it in one
        material = printer.materials.get(global_material__name__iexact=stl_data['material'])
        colour = material.colours.get(global_colours__name__iexact=stl_data['colour'])
 
        print('material price length:')
        print(material.price_length)

        print('Color coefficient:')
        print(colour.price_coefficient)

        energy_use = (cura_data['print_s'] / 3600) * self.power
        price_time_to_print = float(self.price_hour) * (cura_data['print_s'] / 3600)
        total_margin_coefficient = (self.price_margin / 100 ) + 1
        price_length_of_filament = float(cura_data['fil_len']) * float(material.price_length)
        price_energy_use = float(energy_use) * float(self.price_energy)
        material_colour_coefficient = colour.price_coefficient 
        
        price_pre_margin = (  float(price_time_to_print)      \
                            + float(price_length_of_filament) \
                            + float(price_energy_use)         \
                            ) * float(material_colour_coefficient)  
        
        print('QUOTE:')

        print('time hours')
        print((cura_data['print_s'] / 3600))
        print('cost hours')
        print(float(self.price_hour))
        print('energy_use')
        print(energy_use)
        print('self.price_energy')
        print(self.price_energy)

        print('price_pre_margin')
        print(price_pre_margin)
        print('price_time_to_print')

        print(price_time_to_print)
        print('price_length_of_filament')
        print(price_length_of_filament)
        print('total_margin_coefficient')
        print(total_margin_coefficient)
        print('price_energy_use')
        print(price_energy_use)       

        price_total = float(price_pre_margin) * float(total_margin_coefficient)

        if price_total < self.price_min:
            price_total = self.price_min
        
        return price_total


    

