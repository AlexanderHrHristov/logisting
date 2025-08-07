import django_filters
from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter

from .models import Supplier
from users.models import AppUser  # или твоя custom user model

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
