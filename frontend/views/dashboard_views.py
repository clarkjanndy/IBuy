from django.views.generic import TemplateView

from . custom_mixins import AdminRequiredMixin
from backend import analytics

__all__ = ['DashboardView']

class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'frontend/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'admin-dashboard'})
        
        # analytics data
        user_count = analytics.user_count()
        sales_sum =  analytics.sales_sum()
        expenses_sum = analytics.expenses_sum()
        profit_sum = sales_sum - expenses_sum
        
        context.update({'users': user_count})
        context.update({'sales': sales_sum})
        context.update({'expenses': expenses_sum})
        context.update({'profit': profit_sum})
        
        return context