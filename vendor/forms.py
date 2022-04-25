# from attr import fields
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit
from .models import Vendor

class VendorSettingsForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ['store_name', 'slug', 'description', 'store_logo_raw']
        # exclude = ['user','created_by','store_logo_thumbnail']
        labels = {        
            'store_logo_raw': 'Change Logo',         
            }

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            HTML('<h2></h2>')
        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field)
            )
        helper.layout.append(Submit('submit','Save',css_class='btn-primary'))
        return helper