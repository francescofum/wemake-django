from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import MaterialOptions
from core.models import MATERIAL_GLOBAL
from core.models import COLOUR_GLOBAL


class MaterialForm(forms.ModelForm):
    '''
        @brief TODO
    '''
    class Meta:
        model = MaterialOptions
        fields = '__all__' 



