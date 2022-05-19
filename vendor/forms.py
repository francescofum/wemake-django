# from attr import fields
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit
from .models import Vendor

class VendorSettingsForm(forms.ModelForm):

    class Meta:
        model = Vendor
        detail_fields = ['store_name', 'slug', 'description', 'store_logo_raw' ]
        shipping_fields = ['lead_time']
        address_fields =  [ 'address_line1', 'address_line2', 'city', 'postal_code', 'country']
        fields = detail_fields + shipping_fields + address_fields
        # exclude = ['user','created_by','store_logo_thumbnail']
        labels = {        
            'store_logo_raw': 'Change Logo',         
            }

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            HTML('<h3>Store Details</h3>')
        )
        for field in self.Meta().detail_fields:
            helper.layout.append(
                Field(field)
            )
        helper.layout.append(
            HTML('<h3>Shipping Info</h3>')
        )
        for field in self.Meta().shipping_fields:
            helper.layout.append(
                Field(field)
            )
        helper.layout.append(
            HTML('<h3>Store Address</h3>')
        )
        for field in self.Meta().address_fields:
            helper.layout.append(
                Field(field)
            )
            
        helper.layout.append(Submit('submit','Save',css_class='btn-primary'))
        return helper