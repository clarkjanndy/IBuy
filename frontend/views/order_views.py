from django.db.models import Q
from django.views.generic import ListView, DetailView

from backend.models import Order

from . custom_mixins import LoginRequiredMixin, AdminRequiredMixin, NormalUserRequiredMixin

__all__ = [
    'OrderList',
    'OrderDetail',
    'OrderDetailTransact',
    'OrderDetailReceipt',
    'MyOrder', 
    'MyOrderDetail',
    'MyOrderDetailPayment',
    'MyOrderDetailReceipt'
] 

# admin views here
class OrderList(AdminRequiredMixin, ListView):
    template_name = 'frontend/admin/order/list.html'
    queryset = Order.objects.prefetch_related('user', 'items', 'items__uniform', 'items__uniform__images', 'payment_option')
    ordering = ('-modified_at')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-orders'})
        return context

    def get_queryset(self):
        # Get current request
        request = self.request
        # Get query params
        params = request.GET

        # Get the desired page size from the request's GET parameter
        page_size = params.get('page_size', self.paginate_by)
        # Set the paginate_by attribute to the desired page size
        self.paginate_by = page_size

        queryset = super().get_queryset()
        # Filter results
        if 'q' in params:
            queryset = queryset.filter(
                Q(ref_no__icontains = params['q']) |
                Q(status__icontains = params['q']) |
                Q(user__last_name__icontains = params['q']) |
                Q(user__first_name__icontains = params['q']) 
            )
        return queryset
    
class OrderDetail(AdminRequiredMixin, DetailView):
    model = Order
    template_name = 'frontend//admin/order/detail.html'
    queryset = Order.objects.prefetch_related('user', 'payment_option', 'payment')
    context_object_name = 'order'
    slug_field = 'ref_no'  # Specify the field to use for the lookup
    slug_url_kwarg = 'ref_no'  # Specify the URL keyword to use for the lookup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-orders'})
        return context

class OrderDetailTransact(OrderDetail):
    template_name = 'frontend/admin/order/detail_transact.html'
    
class OrderDetailReceipt(OrderDetail):
    template_name = 'frontend/admin/order/detail_receipt.html'
    
# normal user views here
class MyOrder(NormalUserRequiredMixin, ListView):
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
    
class MyOrderDetail(NormalUserRequiredMixin, DetailView):
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
    








    
