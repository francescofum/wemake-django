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
        fields = ['first_name', 'last_name', 'email', 'address', 'address2', 'country', 'city', 'zipcode' ]

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
