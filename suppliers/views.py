import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View)
from django_filters.views import FilterView

from logisting.mixins import (LegalOnlyMixin, LogisticsManagerRequiredMixin,
                              LogisticsOrManagerRequiredMixin)

from .filters import ContractFilter, SupplierFilter
from .forms import ContractForm, DeliveryScheduleForm, SupplierForm
from .models import Contract, DeliverySchedule, Supplier

User = get_user_model()



# Suppliers Register Views

class SupplierListView(LoginRequiredMixin, LegalOnlyMixin, LogisticsOrManagerRequiredMixin, FilterView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 20
    filterset_class = SupplierFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_logistics_manager'] = user.groups.filter(name='Logistics Manager').exists()
        return context


class SupplierCreateView(LoginRequiredMixin, LogisticsOrManagerRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/templates/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier-list')


class SupplierUpdateView(LoginRequiredMixin, LogisticsOrManagerRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/templates/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier-list')


class SupplierDeleteView(LoginRequiredMixin, LogisticsManagerRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'suppliers/templates/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers:supplier-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Доставчикът беше изтрит успешно.')
        return super().delete(request, *args, **kwargs)


# Contracts Register Views

class ContractListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contract
    template_name = 'suppliers/templates/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_filter = ContractFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = contract_filter
        context['contracts'] = contract_filter.qs
        return context

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=['Legal', 'Logistics', 'Logistics Manager']).exists()


class ContractCreateView(LoginRequiredMixin, LegalOnlyMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'suppliers/templates/contract_form.html'
    success_url = reverse_lazy('suppliers:contract-list')


class ContractUpdateView(LoginRequiredMixin, LegalOnlyMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'suppliers/templates/contract_form.html'
    success_url = reverse_lazy('suppliers:contract-list')


class ContractToggleActiveView(LoginRequiredMixin, LegalOnlyMixin, View):
    def post(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        contract.is_active = not contract.is_active
        contract.save()
        messages.success(request, "Статусът на договора беше променен.")
        return redirect('suppliers:contract-list')


class ContractDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        contract.delete()
        messages.success(request, "Договорът беше изтрит.")
        return redirect('suppliers:contract-list')


# DeliverySchedule - Views


class DeliveryScheduleListView(ListView):
    model = DeliverySchedule
    template_name = "suppliers/delivery_schedule.html"
    context_object_name = "schedules"

    def get_queryset(self):
        qs = DeliverySchedule.objects.select_related('supplier', 'supplier__responsible_logistic').all()

        date = self.request.GET.get('date')
        supplier = self.request.GET.get('supplier')

        if date:
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                qs = qs.filter(date=date_obj)
            except ValueError:
                pass  # игнорирай грешни дати

        if supplier:
            try:
                qs = qs.filter(supplier_id=int(supplier))
            except ValueError:
                pass  # игнорирай грешни id-та

        return qs.order_by('date', 'hour')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Списък с всички доставчици за филтъра
        context['suppliers'] = Supplier.objects.all()

        # Уникални дати за филтъра
        dates = DeliverySchedule.objects.order_by('date').values_list('date', flat=True).distinct()
        context['workdays'] = dates

        # Групиране по дата за таблицата
        schedules_by_day = {}
        for schedule in context['schedules']:
            schedules_by_day.setdefault(schedule.date, []).append(schedule)
        context['schedules_by_day'] = schedules_by_day

        return context


class DeliveryScheduleCreateView(CreateView):
    model = DeliverySchedule
    form_class = DeliveryScheduleForm
    template_name = "suppliers/delivery_schedule_form.html"
    success_url = reverse_lazy('suppliers:delivery_schedule_list')


class DeliveryScheduleUpdateView(UpdateView):
    model = DeliverySchedule
    form_class = DeliveryScheduleForm
    template_name = "suppliers/delivery_schedule_form.html"
    success_url = reverse_lazy('suppliers:delivery_schedule_list')
