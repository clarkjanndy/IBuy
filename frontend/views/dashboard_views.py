from django.views.generic import TemplateView
from django.conf import settings
from . custom_mixins import AdminRequiredMixin
from backend import analytics

__all__ = ['DashboardView']

class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'frontend/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'admin-dashboard'})
        context.update({'MEDIA_URL': settings.MEDIA_URL})
        
        # analytics data
        user_count = analytics.user_count()
        sales_sum =  analytics.sales_sum()
        expenses_sum = analytics.expenses_sum()
        profit_sum = sales_sum - expenses_sum
        capitals = analytics.capitals()
        order_recent = analytics.order_recent
        uniform_sales_ranking = analytics.uniform_sales_ranking()
     
        
        context.update({'users': user_count})
        context.update({'sales': sales_sum})
        context.update({'expenses': expenses_sum})
        context.update({'profit': profit_sum})
        context.update({'capitals': capitals})
        context.update({'order_recent': order_recent})
        context.update({'uniform_sales_ranking': uniform_sales_ranking})
        
        return context