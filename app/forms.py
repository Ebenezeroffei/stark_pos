from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """ A form that creates a form """

    class Meta:
        model = Product
        fields = ['name','quantity','unit_price','unit_cost','unit','image']
        widgets = {
            'name': forms.TextInput(attrs = {
                'class': 'form-control'
            }),
            'unit_price': forms.NumberInput(attrs = {
                'class': 'form-control'
            }),
            'unit_cost': forms.NumberInput(attrs = {
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs = {
                'class': 'form-control'
            }),
            'unit': forms.Select(attrs = {
                'class': 'form-control'
            })
        }
