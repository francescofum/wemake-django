from django.db import models
from printer.models import * 

class GLOBAL_MATERIALS(models.Model):
    '''
        A class representing global materials.
    '''
    name = models.CharField(max_length=255)
    density = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)

    def __str__(self):
        return self.name
    
class GLOBAL_COLOURS(models.Model):
    '''
        A class representing global colours.
    '''
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name