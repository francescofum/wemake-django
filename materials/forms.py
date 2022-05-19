from django import forms
from django.forms.widgets import TextInput

from .models import Material, Colour
from core.models import GLOBAL_MATERIALS
from core.models import GLOBAL_COLOURS


class MaterialForm(forms.ModelForm):
    '''
        @brief TODO
    '''
    class Meta:
        model = Material
        fields = '__all__' 
        exclude = ['printers','vendor']
        labels = {'quantity': 'In stock',
                  'global_material':'Material'}



class ColourForm(forms.ModelForm):
    '''
        @brief TODO
    '''

    def __init__(self, *args, **kwargs):

        # This is kinda hacky but also not hacky. 
        # I wanted to stick with forms.ModelForm rather
        # than creating my own custom form...
        # So what I did is kept the form like it was generated
        # by django, and then filtered the dropdown (the one
        # with foreign keys pointing to the colour)
        # and just kept one colour each time. 
        # Then I set the initial value to the only colour
        # left and finally disabled the dropdown. 
        # To be honest this might need a custom form 
        # but this will do for now.

        self.colour_id = kwargs.pop('colour_id', None)

        super().__init__(*args, **kwargs)
        # Exclude all colours apart from the selected one.
        exclude = [str(colour.id) for colour in GLOBAL_COLOURS.objects.all() if colour.id is not self.colour_id]

        # material = Material.objects.get(pk=id)
        # for colour in material.colours.all():


        self.fields['global_colours'].queryset = GLOBAL_COLOURS.objects.exclude(id__in=exclude)
        self.fields['global_colours'].initial = self.colour_id 
        self.fields['global_colours'].disabled = True

    


      
      

    class Meta:
        model = Colour
        fields = '__all__' 
        exclude = ['owned_by','discount']
        labels = {'global_colours':'Colour'}

    def get_initial(self) -> list:
        '''
            TODO
        '''
        if self.printer is not None:
            return [material.id for material in self.vendor.materials.all()]
        else:
            return []
