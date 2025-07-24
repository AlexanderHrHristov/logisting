from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Supplier
from .forms import SupplierForm



# class SupplierListView(LoginRequiredMixin, ListView):
#     model = Supplier
#     template_name = 'suppliers_app/supplier_list.html'
#     context_object_name = 'suppliers'

#     def get_queryset(self):
#         qs = Supplier.objects.all()
#         count = qs.count()
#         print(f"DEBUG Suppliers: Found {count} suppliers")
#         if count == 0:
#             print("DEBUG Suppliers: НЯМА ДОСТАВЧИЦИ В QuerySet")
#         else:
#             for s in qs:
#                 print(f"Supplier: {s} (is_active={s.is_active})")
#         return qs

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    count = suppliers.count()
    print(f"DEBUG Suppliers: Found {count} suppliers")
    if count == 0:
        print("DEBUG Suppliers: НЯМА ДОСТАВЧИЦИ В QuerySet")
    else:
        for s in suppliers:
            print(f"Supplier: {s} (is_active={s.is_active})")

    context = {
        'suppliers': suppliers,
    }
    return render(request, 'suppliers_app/supplier_list.html', context)



class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers_app/supplier_form.html'
    success_url = reverse_lazy('suppliers')  # <-- това гарантира redirect след Save

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добави доставчик'
        return context

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers_app/supplier_form.html'
    success_url = reverse_lazy('suppliers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирай доставчик'
        return context

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'suppliers_app/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers')
