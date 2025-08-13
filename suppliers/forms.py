from django import forms
from .models import Supplier, Contract, DeliverySchedule
#from internationalflavor.vat_number.forms import VATNumberFormField



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
        fields = ['supplier', 'day', 'hour']

    def clean_hour(self):
        value = self.cleaned_data.get('hour')  # това вече е datetime.time обект

        if value is None:
            raise forms.ValidationError("Моля, въведете валиден час за доставка.")

        # Пример за проверка: да не е в миналото
        import datetime
        now_time = datetime.datetime.now().time()
        if value < now_time:
            raise forms.ValidationError("Часът за доставка не може да е преди текущия час.")

        return value
