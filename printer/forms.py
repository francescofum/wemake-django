from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Printer
from vendor.models import Vendor
from materials.models import MaterialOptions


class PrinterForm(forms.ModelForm):
    '''
        @brief TODO
    '''
    class Meta:
        model = Printer 
        fields = [
            'name',
            'is_active',
            'slug',
            'description',
            'price_energy',
            'price_length',
            'price_min',
            'price_hour',
            'price_margin',
            'tray_length',
            'tray_width',
            'tray_height',
            'power',
            'config',
        ]
        labels = {
        'is_active': 'Status',
        }


class MaterialForm(forms.Form):

    def __init__(self, *args, **kwargs):
        '''
            @brief A form representing the materials a printer can have.
            The for will check what materials the user has available and
            displays them as checkboxes. This is not a required field as 
            a printer can have no materials assigned to it.  
        '''
        
        self.vendor = kwargs.pop('vendor', None)
        self.printer = kwargs.pop('printer', None)

        MATERIALS = list([str(id),material] for id,material in self.vendor.get_unique_materials())
        super().__init__(*args, **kwargs)
        self.fields['materials'] = forms.MultipleChoiceField(initial=self.get_initial(),
                                    choices = MATERIALS,
                                    widget=forms.CheckboxSelectMultiple)
        self.fields['materials'].required = False

    def get_initial(self) -> list:
        '''
            @brief Returns a list of material ids. 
            Useful for checking the material checkboxes
            which the printer already has.
            @return A list containing the MATERIAL_GLOBAL ids of each material.
        '''
        if self.printer is not None:
            return [material.material.id for material in self.printer.materials.all()]
        else:
            return []

 
    
