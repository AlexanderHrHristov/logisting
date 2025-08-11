from django import forms

from datetime import date

from internationalflavor.vat_number.forms import VATNumberFormField

from suppliers.models import Supplier, Contract, DeliverySchedule


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'vat_number',
            'email',
            'phone',
            'contact_person',
            'delivery_method',       # Тук трябва да е точно това име
            'responsible_logistic',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'vat_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),  # Избор от dropdown
            'responsible_logistic': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'signed_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }



class DeliveryScheduleForm(forms.ModelForm):
    class Meta:
        model = DeliverySchedule
        fields = ['day', 'time_slot', 'supplier', 'logistics_responsible', 'note']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        time_slot = cleaned_data.get('time_slot')

        if day and time_slot:
            count = DeliverySchedule.objects.filter(day=day, time_slot=time_slot).count()
            # Ако е създаване (няма pk) и вече има 8 записи
            if self.instance.pk is None and count >= 8:
                raise forms.ValidationError("Този слот вече е запълнен с максимален брой доставчици (8).")
        return cleaned_data
