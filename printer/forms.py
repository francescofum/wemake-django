from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit, Div

from .models import Printer
from vendor.models import Vendor
from materials.models import Material


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

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            HTML('<h2>Printer Settings</h2>')
        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field)
            )
        helper.layout.append(Submit('submit','Save',css_class='btn-primary'))
        helper.form_tag = False
        return helper


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

        MATERIALS = list([str(material.id),material.global_material.name] for material in self.vendor.materials.all())

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
            @return A list containing the GLOBAL_MATERIALS ids of each material.
        '''
        if self.printer is not None:
            return [material.id for material in self.printer.materials.all()]
        else:
            return []

 
    
