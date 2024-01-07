from django.db.models import Q
from django.views.generic import ListView, DetailView

from backend.models import Order, PaymentOption

from . custom_mixins import LoginRequiredMixin

__all__ = [
    'MyOrder', 
    'MyOrderDetail',
    'MyOrderDetailPayment',
    'MyOrderDetailReceipt'
] 

# normal user views here
class MyOrder(LoginRequiredMixin, ListView):
    template_name = 'frontend/order/list.html'
    queryset = Order.objects.prefetch_related('user', 'items', 'items__uniform', 'items__uniform__images', 'payment_option')
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'my-orders'})
        return context

    def get_queryset(self):
        # Get current request
        request = self.request
        # Get query params
        params = request.GET
        queryset = super().get_queryset()
        
        if 'tab' in params:
            queryset = queryset.filter(status = params['tab'])
            
        if 'q' in params:
            queryset = queryset.filter(
                Q(ref_no__icontains = params['q']) |
                Q(items__uniform__name__contains = params['q'])
            )
    
        return queryset.filter(user = request.user)
    
class MyOrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'frontend/order/detail.html'
    queryset = Order.objects.prefetch_related('user', 'payment_option', 'payment')
    context_object_name = 'order'
    slug_field = 'ref_no'  # Specify the field to use for the lookup
    slug_url_kwarg = 'ref_no'  # Specify the URL keyword to use for the lookup

    def get_queryset(self):
        # Get current request
        request = self.request
        queryset = super().get_queryset()    
        return queryset.filter(user = request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'my-orders'})
        return context
    
class MyOrderDetailPayment(MyOrderDetail):
    template_name = 'frontend/order/detail_pay.html'
    
class MyOrderDetailReceipt(MyOrderDetail):
    template_name = 'frontend/order/detail_receipt.html'
    








    
