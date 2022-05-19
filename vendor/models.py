'''
Model description

Store:
* Store Name 
* Store Slug 
* Store Phone (later)
* Store gallery (imgages )
* Store logo 
* Store Description 

Location:
- Street
- Street 2
- City/Town 
- Postcode/Zip
- Country 
- State/Country 

Payment:
- more though required.. (later)

Shipping: ... this requires a bit of thought (later)
- Processing time 
- Shipping Type ?

Store Policies: (later)
        
'''


from io import BytesIO
from PIL import Image

from django.core.files import File
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q




# User model 


# Vendor model 
class Vendor(models.Model):
    '''
        How to query as a vendor:
        User case: you need to identify all the printers
        of a given vendor which can PLA BLUE
    '''
    created_at                  = models.DateTimeField(auto_now_add=True)
    created_by                  = models.OneToOneField(User,related_name='vendor', on_delete=models.CASCADE, null=True)
    store_name                  = models.CharField(max_length=255,blank=True, null=True)
    slug                        = models.SlugField(blank=False, null=False)
    description                 = models.TextField(blank=True, null=True)
    store_logo_raw              = models.ImageField(null=True, blank=True)
    store_logo_thumbnail        = models.ImageField(null=True, blank=True)

    DELIVERY_CHOICES = (
        ('NEXTDAY', "Next day delivery"),
        ('1TO3BUS', "1-3 business days"),
        ('WEEK', "7 business days")
    )

    lead_time = models.CharField(choices=DELIVERY_CHOICES,max_length=50,default='WEEK')

    # All this could be in a seperate "address" model
    address_line1       = models.CharField(max_length=255,blank=True, null=True)
    address_line2       = models.CharField(max_length=255,blank=True, null=True)
    city                = models.CharField(max_length=255,blank=True, null=True)
    postal_code         = models.CharField(max_length=255,blank=True, null=True)
    country             = models.CharField(max_length=255,blank=True, null=True)
    
    # TODO store gallery

    class Meta:
        ordering = (['created_by'])

    def __str__(self):
        return self.store_name


    def get_thumbnail(self):
        if self.store_logo_thumbnail:
            return self.store_logo_thumbnail.url
        else:
            if self.store_logo_raw: 
                self.store_logo_thumbnail = self.make_thumbnail()
                self.save()

                return self.store_logo_thumbnail.url
            else: 
                return 'https://via.placeholder.com/240x240.jpg'


    def make_thumbnail(self, size=(300,200)):
        image = self.store_logo_raw 
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def get_compatible_printers(self,sel_material:str,sel_colour:str,size:dict) -> list:
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
        vendor = Vendor.objects.get(id=self.id)

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
                        if colour.global_colours.name == sel_colour and colour.stock == True:
                            # check if printer can handle model dims
                            if( (size['x'] < printer.tray_length * scale ) and 
                                (size['y'] < printer.tray_width  * scale )  and 
                                (size['z'] < printer.tray_height * scale )): 
                                compatible_printers.append(printer)

                    printers.add(printer)

        return list(printers)


    # def get_unique_materials(self) -> list:
    #     '''
    #         @brief: Get all the materials of a given vendor. 
    #         @return: a list of strings, each string is a material name. 
    #     '''
    #     vendor = Vendor.objects.get(id=self.id)
    #     materials = list()
    #     for material in vendor.materials.all():
    #         if material.material.id not in materials:
    #             materials.append((material.material.id,material.material.name))

    #     return list(set(materials))
        return list(compatible_printers)
    
    def get_unique_materials(self) -> list:
        '''
            @brief: Get all the materials of a given vendor. 
            @return: a list of strings, each string is a material name. 
        '''
        vendor = Vendor.objects.get(id=self.id)
        materials = list()
        for material in vendor.materials.all():
            if material.material.id not in materials:
                materials.append((material.material.id,material.material.name))

        return list(set(materials))

    def serialize_materials_for_print_preview(self):
        '''
        For a given vendor will return a json with materials and colours
            ::
                {1: {'colours': 
                        {1: 'RED',
                        2: 'BLUE',
                        3: 'PURPLE',
                        4: 'ORANGE',
                        5: 'WHITE',
                        6: 'BLACK'},
                        'name': 'PLA'},
                3: {'colours': 
                        {7: 'RED',
                        8: 'BLUE',
                        9: 'PURPLE',
                        10: 'ORANGE',
                        11: 'WHITE',
                        12: 'BLACK'},
                        'name': 'ABS'}}

        This could be achieved with an inner join, but this was faster to implement. 
        Currently this is used in order to make the python wemake compatible
        with print preview, but could change in the future. 

        '''
        materials_json = {}
        materials = self.materials.all()
        for material in materials:
            materials_json[material.global_material.id] = {}
            materials_json[material.global_material.id]['name'] = material.global_material.name
            materials_json[material.global_material.id]['colours'] = {}
            for colour in material.colours.all():
                if(colour.stock):
                    materials_json[material.global_material.id]['colours'][colour.id] = colour.global_colours.name
    
        return materials_json
    
    def get_materials(self,material:str):
        '''
            @brief: Returns the all the material options based on a 
            given material. 
            i.e material="ABS" will return all the abs colours.
            @param[material]: A string representing the material name . 
            @return: A list of QuerySet Material objects. 
        '''
        vendor = Vendor.objects.get(id=self.id)
        return vendor.materials.filter(material__name__iexact=material) 
    



    

