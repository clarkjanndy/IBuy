from django.db.models import Q
from django.views.generic import ListView, TemplateView, DetailView

from backend.models import Uniform, Category, PaymentOption

from . custom_mixins import AdminRequiredMixin, LoginRequiredMixin

__all__ = [
    'UniformBrowse', 
    'UniformView', 
    'UniformList', 
    'UniformCreate', 
    'UniformDetail', 
    'UniformImages', 
    'UniformEdit'
] 

# normal user views here
class UniformBrowse(LoginRequiredMixin, ListView):
    template_name = 'frontend/uniform/list.html'
    queryset = Uniform.objects.select_related('category').filter(status='active')
    paginate_by = 12
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({'current_page': 'uniforms'})
        context.update({'categories': Category.objects.all()})
        return context

    def get_queryset(self):
        # Get current request
        request = self.request
        # Get query params
        params = request.GET
        queryset = super().get_queryset()
        
        if 'category' in params:
            queryset = queryset.filter(
                Q(category__name__icontains = params['category']) 
            )
        
        # filter results here
        if 'q' in params:
            queryset = queryset.filter(
                Q(name__icontains = params['q']) |
                Q(extra_name__icontains = params['q']) 
            )
        
        return queryset
    
class UniformView(LoginRequiredMixin, DetailView):
    model = Uniform
    template_name = 'frontend/uniform/detail.html'
    context_object_name = 'uniform'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'payment_options': PaymentOption.objects.all()})      
        context.update({'current_page': 'uniforms'})
        return context
    
# admin management views here
class UniformList(AdminRequiredMixin, ListView):
    template_name = 'frontend/admin/uniform/list.html'
    queryset = Uniform.objects.select_related('category').all()
    paginate_by = 10
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-uniforms'})
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
        # filter results here
        if 'q' in params:
            queryset = queryset.filter(
                Q(name__icontains = params['q']) |
                Q(extra_name__icontains = params['q']) |
                Q(category__name__icontains = params['q'])
            )
        
        return queryset

class UniformCreate(AdminRequiredMixin, TemplateView):
    template_name = 'frontend/admin/uniform/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"categories": Category.objects.all()})
        context.update({'current_page': 'manage-uniforms'})
        return context
    
class UniformDetail(AdminRequiredMixin, DetailView):
    model = Uniform
    template_name = 'frontend/admin/uniform/detail.html'
    context_object_name = 'uniform'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-uniforms'})
        return context

class UniformEdit(AdminRequiredMixin, DetailView):
    model = Uniform
    template_name = 'frontend/admin/uniform/edit.html'
    context_object_name = 'uniform'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"categories": Category.objects.all()})
        context.update({'current_page': 'manage-uniforms'})
        return context
    
class UniformImages(AdminRequiredMixin, DetailView):
    model = Uniform
    template_name = 'frontend/admin/uniform/detail_images.html'
    context_object_name = 'uniform'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-uniforms'})
        return context
    




    
