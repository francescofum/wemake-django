from django.shortcuts import render


from materials.models import MaterialOptions

from vendor.models import Vendor
from .forms import  MaterialForm


def material_details(request,id:int=None): 
    '''
        @brief: TODO
    '''
    vendor = request.user.vendor

    # Either display an existing material,
    # or a blank form for a new material.
    if request.method == "GET":
        if id is not None:
            materialOption = MaterialOptions.objects.get(pk=id)
            material_form = MaterialForm(instance=materialOption) 
        else:
            material_form = MaterialForm()
            context = {'material_form':material_form}

    # POST means we're either adding a material, 
    # updating a material or deleting one. 
    # If an id has been specified then we are editing one.
    if request.method == "POST":
        material_form = MaterialForm(request.POST)
        
        if material_form.is_valid():
            # Update or delete an existing material option
            if id is not None:  
                # TODO: Check that the material actually exists.
                materialOption = MaterialOptions.objects.get(pk=id) 
                if 'update' in request.POST:
                    material_form = MaterialForm(request.POST,instance=materialOption) 
                    material_form.save()
                if 'delete' in request.POST:
                    materialOption.delete()
                    material_form = MaterialForm()
            # Add a new material option
            else: 
                materialOption = material_form.save(commit=False)
                materialOption.vendor = vendor
                materialOption.save()
        else:
            # TODO: Handle not valid form.
            print("NOT OK")

    # Render the view
    context = {'material_form':material_form}
    return render(request,'material/material_form.html',context)