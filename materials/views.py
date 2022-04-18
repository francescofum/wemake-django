from django.shortcuts import render


from materials.models import MaterialOptions
from .models import Printer
from vendor.models import Vendor
from .forms import  MaterialForm


def material_details(request,id:int=None): 
    pass