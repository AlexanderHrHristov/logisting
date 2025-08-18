from django import forms
from django.contrib.auth import get_user_model

from .models import Contract, DeliverySchedule, Supplier, PickupSchedule


User = get_user_model()


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'vat_number',
            'email',
            'phone',
            'contact_person',
            'delivery_method',  # Тук трябва да е точно това име
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
    date = forms.DateField(
        widget=forms.Select(),
        label="Дата на доставка"
    )

    class Meta:
        model = DeliverySchedule
        fields = ['supplier', 'date', 'hour', 'note']
        widgets = {
            'hour': forms.TimeInput(attrs={'type': 'time', 'min': '08:00', 'max': '17:00'}),
            'note': forms.Textarea(attrs={'rows': 2}),
            'supplier': forms.Select(),
            'logistics_responsible': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Филтрираме само доставчици с вид на доставка "На място"
        from .models import Supplier
        self.fields['supplier'].queryset = Supplier.objects.filter(delivery_method='delivery')

        # Генериране на дати за следващите 2 седмици (само работни дни)
        import datetime
        today = datetime.date.today()
        dates = []
        for i in range(14):  # 2 седмици
            day = today + datetime.timedelta(days=i)
            if day.weekday() < 5:  # 0=пон, 4=пет
                dates.append((day, day.strftime("%A, %d %b %Y")))
        self.fields['date'].widget.choices = dates


class PickupScheduleForm(forms.ModelForm):
    class Meta:
        model = PickupSchedule
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'thermolabile': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'narcotic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
        }
