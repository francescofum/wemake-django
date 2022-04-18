from django.shortcuts import render


from materials.models import MaterialOptions
from .models import Printer
from vendor.models import Vendor
from .forms import  MaterialForm


def material_details(request,id:int=None): 

    # Either display an existing material,
    # or a blank form for a new material.
    if request.method == "GET":
        if id is not None:
            pass
            # material = Printer.objects.get(pk=id)
            # printer_form = PrinterForm(instance = printer,prefix="printer")
            # material_form = MaterialForm(vendor=vendor,printer=printer,prefix="material")
        else:
            material_form = MaterialForm()