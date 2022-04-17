# from attr import fields
from django import forms

from .models import Vendor

class VendorSettingsForm(forms.ModelForm):


    store_name  = forms.CharField()
    slug        = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea) 

    class Meta:
        model = Vendor
        fields = [
            'store_name',
            'slug',
            'description'
        ]

    def clean_store_name(self, *args, **kwargs):
        store_name = self.cleaned_data.get("store_name")
        if not "raul" in store_name:
            raise forms.ValidationError("Pretty lame")
        return store_name