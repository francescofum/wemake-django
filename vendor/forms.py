# from attr import fields
from cProfile import label
from django import forms

from .models import Vendor

class VendorSettingsForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = '__all__'
        exclude = ['user','created_by','store_logo_thumbnail']
        labels = {        
            'store_logo_raw': 'Change Logo',         
            }

