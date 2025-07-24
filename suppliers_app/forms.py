from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'contact_person', 'delivers_to_us', 'responsible_logistic']
        widgets = {
            'delivers_to_us': forms.RadioSelect(choices=Supplier.DELIVERY_CHOICES)
        }