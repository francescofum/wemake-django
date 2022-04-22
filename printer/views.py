from django.shortcuts import render


from materials.models import MaterialOptions

from .models import Printer
from vendor.models import Vendor
from .forms import PrinterForm, MaterialForm
from django.contrib.auth.decorators import login_required


def printer_details(request,id:int=None): 
    '''
        @brief Renders a printer form. The printer form
        allows the user to either add  new printer or 
        update an existing one depending on the value of
        'id'. 
        @param[id] The id of a printer, defaults to 'None' which
        means a new printer.
    '''
    vendor = request.user.vendor

    # POST means we're either adding a printer, 
    # updating a printer or deleting one. 
    # If an id has been specified then we are editing one.
    if request.method == 'POST':
        printer_form = PrinterForm(request.POST,prefix="printer")
        
        if printer_form.is_valid():
            if id is not None:  
                # TODO: Check that the printer actually exists. 
                printer = Printer.objects.get(pk=id)
                printer_form = PrinterForm(request.POST,instance=printer,prefix="printer") 
                printer_form.save()
            else:
                printer = printer_form.save(commit=False)
                printer.vendor = vendor
                printer.save()
        else:
            # TODO: Handle not valid form.
            print("NOT OK")
        
        # Assign the material to the printer.
        # This is done by first unassigning all materials. 
        # Then assign only the ones that are selected. 
        # TODO: Optimise query. 
        material_form = MaterialForm(request.POST,vendor=vendor,printer=printer,prefix="material")
        if material_form.is_valid():

            material_ids = material_form.cleaned_data.get("materials")
            materials = MaterialOptions.objects.filter(material__pk__in=material_ids, vendor__pk__iexact=vendor.pk)
            for material in printer.materials.all():
                printer.materials.remove(material)
            for material in materials:
                printer.materials.add(material)
        else:
            print(material_form.errors.as_data()) 

    # Either display an existing printer,
    # or a blank form for a new printer.
    if request.method == "GET":
        if id is not None:
            printer = Printer.objects.get(pk=id)
            printer_form = PrinterForm(instance = printer,prefix="printer")
            material_form = MaterialForm(vendor=vendor,printer=printer,prefix="material")
        else:
            printer_form = PrinterForm(prefix="printer")
            material_form = MaterialForm(vendor=vendor,prefix="material")

    # Render the form 
    context = {'printer_form':printer_form, 'material_form':material_form}
    return render(request,'printer/printer_form.html',context)

@login_required
def printer_dashboard(request):
    '''
        Main entry point for vendor (dashboards/orders etc)
    '''

    vendor = request.user.vendor
    print('vendor:')
    print(vendor)
    print('vendor.get_unique_materials:')
    printers = vendor.printers.all()
    print(printers)

    if(request.method == 'GET'):
        context = {
            'vendor':vendor,
            'printers':printers
        }        
        return render(request,'printer/printer_dashboard.html', context)