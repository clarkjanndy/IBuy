from django.db.models import Q
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from backend.models import User

from .custom_mixins import AdminRequiredMixin, LoginRequiredMixin

__all__ = ['UserList', 'UserCreate', 'UserDetail', 'UserMyProfile'] 

class UserList(AdminRequiredMixin, ListView):
    template_name = 'frontend/admin/user/list.html'
    queryset = User.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-user'})
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
                Q(email__icontains = params['q']) |
                Q(first_name__icontains = params['q']) |
                Q(middle_name__icontains = params['q']) |
                Q(last_name__icontains = params['q']) 
            )
        return queryset

class UserCreate(AdminRequiredMixin, TemplateView):
    template_name = 'frontend/admin/user/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-user'})
        return context
    
class UserDetail(AdminRequiredMixin, DetailView):
    model = User
    template_name = 'frontend/admin/user/detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-user'})
        return context
    
class UserMyProfile(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/my-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'my-profile'})
        return context




    
