from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django_filters.views import FilterView
from .models import Supplier, Contract, DeliverySchedule
from .forms import SupplierForm, ContractForm, DeliveryScheduleForm
from logisting.mixins import (
    LegalOnlyMixin,
    LogisticsManagerRequiredMixin,
    LogisticsOrManagerRequiredMixin,
)
from .filters import SupplierFilter, ContractFilter
from django.shortcuts import redirect, get_object_or_404



class SupplierListView(LoginRequiredMixin, LegalOnlyMixin, LogisticsOrManagerRequiredMixin, FilterView):
    model = Supplier
    template_name = 'suppliers/templates/supplier_list.html'
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


class DeliveryScheduleListView(LoginRequiredMixin, ListView):
    model = DeliverySchedule
    template_name = 'suppliers/templates/delivery_schedule.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        qs = super().get_queryset()
        day = self.request.GET.get('day')
        if day:
            qs = qs.filter(day=day)
        return qs.order_by('day', 'time_slot')


class DeliveryScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DeliverySchedule
    form_class = DeliveryScheduleForm
    template_name = 'suppliers/templates/delivery_schedule_form.html'
    success_url = reverse_lazy('delivery_schedule_list')

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=['Logistics', 'Logistics.manager']).exists()


class DeliveryScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DeliverySchedule
    form_class = DeliveryScheduleForm
    template_name = 'suppliers/templates/delivery_schedule_form.html'
    success_url = reverse_lazy('delivery_schedule_list')

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=['Logistics', 'Logistics.manager']).exists()
