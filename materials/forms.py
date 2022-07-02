from django import forms
from django.forms.widgets import TextInput
from crispy_forms.helper import FormHelper
from .models import Material, Colour
from core.models import GLOBAL_MATERIALS
from core.models import GLOBAL_COLOURS

class MaterialForm(forms.ModelForm):
    '''
        @brief TODO
    '''

    def __init__(self,*args, **kwargs):
        
        self.material_obj = kwargs.get('instance', None)

        #Initialise parent classes after poping "instance"
        super().__init__(*args, **kwargs)

        if self.material_obj is not None:


            self.material_name = self.material_obj.global_material.name
            self.fields['global_material'].widget =  self.fields['global_material'].hidden_widget()
        else:
            # display a dropdown with all the materiasl TODO remove the ones already set.
            self.material_name = "ALL"




    
    
    class Meta:
        model = Material
        fields = '__all__'
        exclude = ['printers','vendor']
        labels = {'global_material':'Material'}
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False

        return helper



class ColourForm(forms.ModelForm):
    '''
        @brief TODO
    '''

    def __init__(self, *args, **kwargs):

        self.colour_id = kwargs.pop('colour_id', None)

        self.colour_name =  GLOBAL_COLOURS.objects.get(pk=self.colour_id)

        super().__init__(*args, **kwargs)
        # Exclude all colours apart from the selected one in the dropdown
        exclude = [str(colour.id) for colour in GLOBAL_COLOURS.objects.all() if colour.id is not self.colour_id]

    
        

        self.fields['global_colours'].queryset = GLOBAL_COLOURS.objects.exclude(id__in=exclude)
        self.fields['global_colours'].initial = self.colour_id 
        self.fields['global_colours'].widget =  self.fields['global_colours'].hidden_widget()

        
    class Meta:
        model = Colour
        fields = '__all__'

        exclude = ['owned_by','discount']
        labels = {'global_colours':'Colour'}

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        return helper

    def get_initial(self) -> list:
        '''
            TODO
        '''
        if self.printer is not None:
            return [material.id for material in self.vendor.materials.all()]
        else:
            return []

