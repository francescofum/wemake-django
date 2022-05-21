from django.shortcuts import render, redirect
from django.db.models import Q

from materials.models import Material
from materials.models import Colour

from .models import Printer
from vendor.models import Vendor
from .forms import PrinterForm, MaterialForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from printPreview.models import STL
import json
from cart.cart import Cart 


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
            # materials = Material.objects.filter(global_material__pk__in=material_ids, vendor__pk__iexact=vendor.pk)
            for material in printer.materials.all():
                printer.materials.remove(material)
            for id in material_ids:
                material = Material.objects.get(pk=id)
                printer.materials.remove(material)
                printer.materials.add(material)
                
        else:
            print(material_form.errors.as_data()) 

        # Redirect to Dashboard 
        return redirect('printer_dashboard')

    # Either display an existing printer,
    # or a blank form for a new printer.
    if request.method == "GET":
        print('in GET request')
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
    printers = vendor.printers.all()

    if(request.method == 'GET'):
        context = {
            'vendor':vendor,
            'printers':printers
        }        
        return render(request,'printer/printer_dashboard.html', context)


def slicer_check(request):
    '''
        slicer_check: takes (1) Upload single stl, then (2) Slices stl (3) Return → table with CURA output      
        if upload new file, delete old one

        request:    POST/GET request from the website
        id:         printer ID, that is used to slice the stl 

        table:      table of the CURA output (time to print, filament length, etc)

    '''
    print('here**************')
    if(request.method == 'GET'):
        # context = {
        #     'vendor':vendor,
        #     'printers':printers
        # }        
        return render(request,'printer/slicer_check.html') #context

    if(request.method == 'POST'):
        stl_data = json.loads(request.POST.get('stl_data'))
        print('stl_data:')
        print(stl_data)

        return render(request,'printer/slicer_check.html') #context

def upload(request,slug):
    '''
        FROM: 
    '''
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        title = file.name
        stl = STL(file=file,pretty_name=title)
        try:
            stl.save()
        except Exception as e:
            print(e)
    
    response = {
        'id': stl.id,
        'filename':stl.file.name,
        'path':stl.file.path,
        'url':stl.file.url,
        'pretty_name': stl.pretty_name,
    }
    return JsonResponse(response,status=200)




def get_available_printers(request,slug):
    '''
        Gets availabe printers, this is called whenever a change is made
        to the stl row. 
        TODO: update the cart with new items. 
    '''
    if request.method == 'POST':
        response = {}
        # Read stl_data
        stl_data = json.loads(request.POST.get('stl_data'))
   
        dims={}
        stl_name        = stl_data['pretty_name']
        stl_filename    = "/" + stl_data['filename']
        stl_id          = stl_data['id']

        id = 1 
        printer = Printer.objects.get(pk=id)
        cura_data = printer.slice(stl_filename)

        response = {
                    'stl_id':stl_id,
                    'cura_data':cura_data,
                    }
                    
    return JsonResponse(response,status=200,safe=False)