from django.views.generic import TemplateView
from .custom_mixins import NotAuthenticatedMixin

from backend.models import Department

__all__ = ['LoginView', 'RegistrationView']

class LoginView(NotAuthenticatedMixin, TemplateView):
    template_name = 'frontend/auth/login.html'


class RegistrationView(NotAuthenticatedMixin, TemplateView):
    template_name = 'frontend/auth/register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'departments': Department.objects.all()})
        return context

