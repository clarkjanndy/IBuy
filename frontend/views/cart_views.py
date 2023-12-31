from django.db.models import Q
from django.views.generic import ListView

from backend.models import Uniform, Category, Cart

from . custom_mixins import LoginRequiredMixin

__all__ = [
    'MyCart', 
] 

# normal user views here
class MyCart(LoginRequiredMixin, ListView):
    template_name = 'frontend/my-cart.html'
    queryset = Cart.objects.select_related('uniform', 'user')
    paginate_by = 12
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({'current_page': 'my-cart'})
        return context

    def get_queryset(self):
        # Get current request
        request = self.request
        # Get query params
        params = request.GET
        queryset = super().get_queryset()
    
        return queryset.filter(user = request.user, status='on-cart')




    
