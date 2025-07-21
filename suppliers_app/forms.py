from django import forms
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
