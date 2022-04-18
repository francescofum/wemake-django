# from attr import fields
from django import forms

from .models import Vendor

class VendorSettingsForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = '__all__'
        exclude = ['user','created_by','store_logo_thumbnail']

    # def clean_store_name(self, *args, **kwargs):
    #     store_name = self.cleaned_data.get("store_name")
    #     if not "raul" in store_name:
    #         raise forms.ValidationError("Pretty lame")
    #     return store_name