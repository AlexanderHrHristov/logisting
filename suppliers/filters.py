import django_filters
from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter

from .models import Supplier, Contract
from users.models import AppUser  # или твоя custom user model

from django import forms


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
    supplier = django_filters.ModelChoiceFilter(
        queryset=Supplier.objects.all(),
        label='Доставчик',
        empty_label='Всички доставчици'
    )

    contract_type = django_filters.ChoiceFilter(
        choices=Contract.CONTRACT_TYPE_CHOICES,
        label='Тип договор'
    )

    expiry_date__gt = django_filters.DateFilter(
        field_name='expiry_date',
        lookup_expr='gt',
        label='Изтичане след',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    expiry_date__lt = django_filters.DateFilter(
        field_name='expiry_date',
        lookup_expr='lt',
        label='Изтичане преди',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    ACTIVE_CHOICES = (
        ('', 'Всички'),
        ('true', 'Да'),
        ('false', 'Не'),
    )

    is_active = django_filters.ChoiceFilter(
        choices=ACTIVE_CHOICES,
        label='Активен',
        method='filter_is_active',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def filter_is_active(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(is_active=True)
        elif value == 'false':
            return queryset.filter(is_active=False)
        return queryset  # '' - всички

    class Meta:
        model = Contract
        fields = ['supplier', 'contract_type', 'expiry_date__gt', 'expiry_date__lt', 'is_active']