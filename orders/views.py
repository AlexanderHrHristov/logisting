from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from logisting.mixins import LogisticsOrManagerRequiredMixin

from .forms import OrderForm
from .models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

class OrderCreateView(LoginRequiredMixin, LogisticsOrManagerRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    permission_message = "Само логистици могат да създават поръчки." # И superusers потребители
    success_url = reverse_lazy('orders:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, LogisticsOrManagerRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    permission_message = "Само логистици могат да редактират поръчки." 
    success_url = reverse_lazy('orders:list')

class OrderDeleteView(LoginRequiredMixin, LogisticsOrManagerRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    permission_message = "Само логистици могат да изтриват поръчки." # И superusers потребители 
    success_url = reverse_lazy('orders:list')
