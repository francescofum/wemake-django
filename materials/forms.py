from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models Material
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
        labels = {'quantity': 'In stock',}



