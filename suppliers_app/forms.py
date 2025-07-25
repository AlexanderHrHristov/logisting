from django import forms

from .models import Supplier
from .models import ExternalWarehouse

from datetime import date



class ExternalWarehouseForm(forms.ModelForm):
    class Meta:
        model = ExternalWarehouse
        fields = ['supplier', 'location', 'volume', 'thermolabile', 'narcotic', 'note', 'driver', 'date']

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date.weekday() in (5, 6):
            raise forms.ValidationError("Няма транспорт в събота и неделя. Моля изберете делничен ден.")
        if selected_date < date.today():
            raise forms.ValidationError("Не може да изберете минала дата.")
        return selected_date




class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'email',
            'phone',
            'contact_person',
            'delivery_method',       # Тук трябва да е точно това име
            'responsible_logistic',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),  # Избор от dropdown
            'responsible_logistic': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
