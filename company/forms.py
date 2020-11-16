from django import forms
from django.contrib.auth.models import User
from app.models import CompanyDetails

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

        widgets = {
            'username': forms.TextInput(attrs = {
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs = {
                'class': 'form-control'
            })
        }


class CompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails
        fields = ['name','mobile1','mobile2','location','image']

        widgets = {
            'name': forms.TextInput(attrs = {
                'class': 'form-control'
            }),
            'mobile1': forms.TextInput(attrs = {
                'class': 'form-control',
                'pattern': '^[\+0-9][0-9\s]+$'
            }),
            'mobile2': forms.TextInput(attrs = {
                'class': 'form-control',
                'pattern': '^[\+0-9][0-9\s]+$'
            }),
            'location': forms.TextInput(attrs = {
                'class': 'form-control',
            })
        }

        labels = {
            'mobile1': "Phone Number 1",
            'mobile2': "Phone Number 2 (Optional)",
            'image': "Company Logo",
            'name': "Company Name",
        }
