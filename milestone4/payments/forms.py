from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'address1', 'address2', 'city', 'postal_code', 'country']
        exclude = ['user',]
        






