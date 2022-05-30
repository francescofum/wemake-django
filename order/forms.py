from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit, Div

from .models import Order


class orderForm(forms.ModelForm):
    '''
        @brief TODO
    '''
    class Meta:
        model = Order 
        fields = ['email', 
                'first_name', 
                'last_name',
                'address', 
                'address2', 
                'city', 
                'country', 
                'zipcode' ,  
                'note',  
                ] 

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            HTML('<h2>Checkout</h2>')
        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field)
            )
        helper.layout.append(Submit('submit','Save',css_class='btn-primary'))
        return helper


class orderForm_Vendor(forms.ModelForm):
    '''
        @brief TODO
    '''
    class Meta:
        model = Order 
        fields = ['status','price_total', 'address', 'address2', 'city', 'country', 'zipcode' , 'email', 'first_name', 'last_name', 'note',  ] 

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            HTML('<h2>Order</h2>')
        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field)
            )
        helper.layout.append(Submit('submit','Save',css_class='btn-primary'))
        return helper