import django_filters
from django import forms
from django_filters import ChoiceFilter, FilterSet, ModelChoiceFilter

from users.models import AppUser  # или твоя custom user model

from .models import Contract, Supplier


class SupplierFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Доставчик')

    delivery_method = ChoiceFilter(
        choices=Supplier.DELIVERY_METHOD_CHOICES,
        label='Метод на доставка'
    )

    responsible_logistic = ModelChoiceFilter(
        queryset=AppUser.objects.exclude(username='admin'),
        label="Отговорен логистик",
        empty_label="Всички"
    )

    class Meta:
        model = Supplier
        fields = ['delivery_method', 'responsible_logistic']


class ContractFilter(django_filters.FilterSet):
    common_attrs = {
        'class': 'form-select form-select-sm',
        'style': 'max-width: 150px; display: inline-block; margin-right: 8px;'
    }

    supplier = django_filters.ModelChoiceFilter(
        queryset=Supplier.objects.all(),
        label='Доставчик',
        widget=forms.Select(attrs=common_attrs)
    )

    contract_type = django_filters.ChoiceFilter(
        choices=Contract.CONTRACT_TYPE_CHOICES,
        label='Тип',
        widget=forms.Select(attrs=common_attrs)
    )

    expiry_date = django_filters.DateFilter(
        label='Изтича след',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={**common_attrs, 'type': 'date'})
    )

    is_active = django_filters.ChoiceFilter(
        choices=(
            ('', 'Всички'),
            ('True', 'Да'),
            ('False', 'Не'),
        ),
        method='filter_is_active',
        label='Активен',
        widget=forms.Select(attrs=common_attrs)
    )

    class Meta:
        model = Contract
        fields = ['supplier', 'contract_type', 'expiry_date', 'is_active']

    def filter_is_active(self, queryset, name, value):
        if value == 'True':
            return queryset.filter(is_active=True)
        elif value == 'False':
            return queryset.filter(is_active=False)
        return queryset