from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    order_date = forms.DateField(
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'form-control datepicker',
                'placeholder': 'дд/мм/гггг',
                'autocomplete': 'off'  # важно за JS datepicker
            }
        ),
        label="Дата на поръчка",
        input_formats=['%d/%m/%Y'],
        required=True
    )

    class Meta:
        model = Order
        fields = ['supplier', 'order_date', 'status', 'note']
        labels = {
            'supplier': 'Доставчик',
            'order_date': 'Дата на поръчка',
            'status': 'Статус',
            'note': 'Бележка',
        }
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }