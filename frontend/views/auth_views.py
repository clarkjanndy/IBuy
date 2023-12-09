from django.views.generic import TemplateView
from .custom_mixins import NotAuthenticatedMixin

__all__ = ['LoginView', 'RegistrationView']

class LoginView(NotAuthenticatedMixin, TemplateView):
    template_name = 'frontend/auth/login.html'


class RegistrationView(NotAuthenticatedMixin, TemplateView):
    template_name = 'frontend/auth/register.html'

