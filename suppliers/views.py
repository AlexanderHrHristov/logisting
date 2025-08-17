from collections import OrderedDict
from datetime import datetime, date as dt_date, timezone, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View)
from django_filters.views import FilterView

from logisting.mixins import (LegalOnlyMixin, LogisticsManagerRequiredMixin,
                              LogisticsOrManagerRequiredMixin)

from .filters import ContractFilter, SupplierFilter
from .forms import ContractForm, DeliveryScheduleForm, SupplierForm, PickupScheduleForm
from .models import Contract, DeliverySchedule, Supplier, PickupSchedule



User = get_user_model()


# Suppliers Register Views

class SupplierListView(LoginRequiredMixin, FilterView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 20
    filterset_class = SupplierFilter

    allowed_groups = ['Logistics', 'Logistics Manager', 'Legal']  # <- добавяме Legal

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        if not set(self.allowed_groups).intersection(user_groups):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_logistics_manager'] = user.groups.filter(name='Logistics Manager').exists()
        return context


class SupplierCreateView(LoginRequiredMixin, LogisticsOrManagerRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier-list')


class SupplierUpdateView(LoginRequiredMixin, LogisticsOrManagerRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier-list')


class SupplierDeleteView(LoginRequiredMixin, LogisticsManagerRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers:supplier-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Доставчикът беше изтрит успешно.')
        return super().delete(request, *args, **kwargs)


# Contracts Register Views

class ContractListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contract
    template_name = 'suppliers/contract_list.html'
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
    template_name = 'suppliers/contract_form.html'
    success_url = reverse_lazy('suppliers:contract-list')


class ContractUpdateView(LoginRequiredMixin, LegalOnlyMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'suppliers/contract_form.html'
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
        qs = DeliverySchedule.objects.select_related(
            'supplier',
            'supplier__responsible_logistic'
        ).all()

        date_param = self.request.GET.get('date')
        supplier = self.request.GET.get('supplier')

        # Филтриране по избрана дата
        if date_param:
            try:
                date_obj = datetime.strptime(date_param, "%Y-%m-%d").date()
                qs = qs.filter(date=date_obj)
            except ValueError:
                pass  # игнорирай грешни дати

        # Филтриране по доставчик
        if supplier:
            try:
                qs = qs.filter(supplier_id=int(supplier))
            except ValueError:
                pass  # игнорирай грешни id-та

        return qs.order_by('date', 'hour')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = dt_date.today()

        # Списък с всички доставчици за филтъра
        context['suppliers'] = Supplier.objects.all()

        # Уникални дати за филтъра (само днешни и бъдещи)
        dates = DeliverySchedule.objects.filter(date__gte=today) \
            .order_by('date') \
            .values_list('date', flat=True) \
            .distinct()
        context['workdays'] = dates

        # Групиране по дата за таблицата (само днешни и бъдещи)
        schedules_by_day = {}
        for schedule in context['schedules']:
            if schedule.date >= today:
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


# PickSchedule - Views

class PickupScheduleListView(ListView):
    model = PickupSchedule
    template_name = "suppliers/pickup_schedule.html"
    context_object_name = "schedules"

    def get_queryset(self):
        queryset = PickupSchedule.objects.select_related('supplier').order_by('date')
        date_filter = self.request.GET.get('date')
        supplier_filter = self.request.GET.get('supplier')

        if date_filter:
            queryset = queryset.filter(date=date_filter)
        if supplier_filter:
            queryset = queryset.filter(supplier_id=supplier_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Списък на всички работни дни (например следващите 14 дни)
        today = timezone.localdate()
        workdays = [today + timedelta(days=i) for i in range(14)]
        context['workdays'] = workdays

        # Списък на доставчици
        context['suppliers'] = Supplier.objects.all()

        # Групиране по ден
        schedules = self.get_queryset()
        schedules_by_day = OrderedDict()
        for schedule in schedules:
            schedules_by_day.setdefault(schedule.date, []).append(schedule)
        context['schedules_by_day'] = schedules_by_day

        return context


class PickupScheduleCreateView(CreateView):
    model = PickupSchedule
    form_class = PickupScheduleForm
    template_name = "suppliers/pickup_schedule_form.html"

    def get_success_url(self):
        return reverse_lazy("suppliers:pickup_schedule_list")


class PickupScheduleUpdateView(UpdateView):
    model = PickupSchedule
    form_class = PickupScheduleForm
    template_name = "suppliers/pickup_schedule.html"

    def get_success_url(self):
        return reverse_lazy("suppliers:pickup_schedule_list")


class PickupScheduleDeleteView(DeleteView):
    model = PickupSchedule
    template_name = "suppliers/pickup_confirm_delete.html"
    success_url = reverse_lazy("suppliers:pickup_schedule_list")