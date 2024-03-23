from django.db.models import Q
from django.views.generic import ListView

from backend.models import Expense

from .custom_mixins import AdminRequiredMixin

__all__ = ['ExpenseList'] 

class ExpenseList(AdminRequiredMixin, ListView):
    template_name = 'frontend/admin/expense/list.html'
    queryset = Expense.objects.all()
    paginate_by = 10
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-expenses'})
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
                Q(name__icontains = params['q']) |
                Q(kind__icontains = params['q']) |
                Q(billing_month__icontains = params['q']) |
                Q(amount__icontains = params['q']) 
            )
        return queryset


    
