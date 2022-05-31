

from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist

from materials.models import Material, Colour
from core.models import GLOBAL_MATERIALS, GLOBAL_COLOURS

from vendor.models import Vendor
from django.contrib.auth.decorators import login_required
from .forms import  MaterialForm, ColourForm


def material_details(request,id:int=None): 
    '''
        @brief: TODO
    '''
    vendor = request.user.vendor

    # ***** GET REQUESTS ******* #

    # Either display an existing material,
    # or a blank form for a new material.
    if request.method == "GET": 
        colour_forms = []
        if id is not None:
            materialOption = Material.objects.get(pk=id)
            material_form = MaterialForm(instance=materialOption)
            # Create a list of colour forms, one for each colour in GLOBAL_COLOURS
            for global_colour in GLOBAL_COLOURS.objects.all():
                try:
                    colour = materialOption.colours.get(global_colours__pk__iexact=global_colour.id)
                    colour_forms.append(ColourForm(colour_id=global_colour.id,instance=colour,prefix=f"colour-{global_colour.id}"))
                except ObjectDoesNotExist:
                    # Colour does not exists so no instance is passed 
                    colour_forms.append(ColourForm(colour_id=global_colour.id,prefix=f"colour-{global_colour.id}"))


        else:
            material_form = MaterialForm()
            for colour in GLOBAL_COLOURS.objects.all():
                colour_forms.append(ColourForm(colour_id=colour.id,prefix=f"colour-{colour.id}"))

    # ***** POST REQUESTS ******* #

    # POST means we're either adding a material, 
    # updating a material or deleting one. 
    # If an id has been specified then we are editing one.
    if request.method == "POST":
        # -----------------------------------
        #           Material Form
        # -----------------------------------
        material_form = MaterialForm(request.POST)
        
        if material_form.is_valid():
            print('material form is valid')
            print('id')
            print(id)
            # Update or delete an existing material option
            if id is not None:  
                # TODO: Check that the material actually exists.
                materialOption = Material.objects.get(pk=id) 
                if 'update' in request.POST:
                    print('update')
                    material_form = MaterialForm(request.POST,instance=materialOption) 
                    material_form.save()
                if 'delete' in request.POST:
                    materialOption.delete()
                    material_form = MaterialForm()
                    return redirect("material_dashboard")
            # Add a new material option
            else: 
                try:
                    materialOption = material_form.save(commit=False)
                    materialOption.vendor = vendor
                    materialOption.save()
                except IntegrityError as e: 
                    return HttpResponse(f"Error combination already exists\n{e}.")
        else:
            # TODO: Handle not valid form.
            print('Material NOK')

            pass

    # -----------------------------------
    #            Colour Form
    # -----------------------------------
    
    if request.method == "POST":
        # Add colours
        # if id is None:
        if "add" in request.POST:
            colour_forms = [ColourForm(request.POST,colour_id=colour.id,prefix=f"colour-{colour.id}") for colour in GLOBAL_COLOURS.objects.all()]
            for form in colour_forms:   
                if not form.is_valid():
                    print(f"Error:{form.errors.as_data}")
                    return HttpResponse(f"\nError:{form.errors.as_data}")
                    # return HttpResponse(f"Form {colour.name} not valid.\nError:{form.errors.as_data}")
                colour = form.save(commit=False)
                colour.owned_by = materialOption
                colour.save()
                

        if "update" in request.POST:
            colour_forms = []
            for global_colour in GLOBAL_COLOURS.objects.all():
                inst = Material.objects.get(pk=id).colours.get(global_colours__pk__iexact=global_colour.id)
                form = ColourForm(request.POST,instance=inst,colour_id=global_colour.id,prefix=f"colour-{global_colour.id}")
                form.save()
                colour_forms.append(form)
        
        return redirect("material_dashboard")


    # Render the view
    context = {'material_form':material_form,'colour_forms':colour_forms}
    return render(request,'material/material_form.html',context)

@login_required
def material_dashboard(request):
    '''
        Main entry point for material_dashboard
    '''

    vendor      = request.user.vendor
    materials   = vendor.materials.all()

    print('materials:')
    print(materials)



    if(request.method == 'GET'):
        context = {
            'vendor':vendor, 
            'materials':materials
        }     
        return render(request,'material/material_dashboard.html', context)


