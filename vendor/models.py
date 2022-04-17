'''
TODO:

    Store:
        - Store Name 
        - Store Slug 
        - Store Phone (later)

        - Store gallery (imgages )
        - Store logo 
        - Store Description 
    
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
        - TODO
'''


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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255,blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # TODO store logo 
    # TODO store gallery

    class Meta:
        ordering = (['created_by'])

    def __str__(self):
        return self.store_name

    def get_compatible_printers(self,material:str,colour:str,size:dict) -> list:
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
        # Scale factor
        scale = 0.9

        # get the vendor 
        vendor = Vendor.objects.get(id=self.id)

        printers = set()
        # Get the printers which can do the material and colour
        for printer in vendor.printers.all():
            # Check if printer can handle colour and material
            if printer.materials.filter(
                Q(colour__name__contains=colour) &
                Q(material__name__contains=material)):
                    
                # check if printer can handle model dims
                if( (size['x'] < printer.tray_length * scale ) and 
                    (size['y'] < printer.tray_width  * scale )  and 
                    (size['z'] < printer.tray_height * scale )): 

                    printers.add(printer)

        return list(printers)
    
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
    
    def get_materials(self,material:str):
        '''
            @brief: Returns the all the material options based on a 
            given material. 
            i.e material="ABS" will return all the abs colours.
            @param[material]: A string representing the material name . 
            @return: A list of QuerySet MaterialOptions objects. 
        '''
        vendor = Vendor.objects.get(id=self.id)
        return vendor.materials.filter(material__name__iexact=material) 



    

