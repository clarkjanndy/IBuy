from frontend import views
from django.urls import path

urlpatterns = [
    # Auth
    path('login', views.LoginView.as_view()),
    path('register', views.RegistrationView.as_view()),
    
    # Uniforms
    path('uniforms', views.UniformBrowse.as_view()),
    
    # Profile
    path('profile', views.UserMyProfile.as_view()),

    # FAQ
    path('faq', views.FAQ.as_view()),

    # About/SystemInformation
    path('about', views.About.as_view()),

    # -------- admin urls starts here --------
    # Dashboard
    path('admin/dashboard', views.DashboardView.as_view()),

    # Users
    path('admin/manage-users', views.UserList.as_view()),
    path('admin/manage-users/create', views.UserCreate.as_view()),
    path('admin/manage-users/<int:pk>', views.UserDetail.as_view()),

    # FAQ
    path('admin/manage-faqs', views.FAQList.as_view()),

    # System Information
    path('admin/manage-system-informations', views.SystemInformationList.as_view()),

    # Uniforms
    path('admin/manage-uniforms', views.UniformList.as_view()),
    path('admin/manage-uniforms/create', views.UniformCreate.as_view()),
    path('admin/manage-uniforms/<int:pk>', views.UniformDetail.as_view()),
     path('admin/manage-uniforms/<int:pk>/edit', views.UniformEdit  .as_view()),
    path('admin/manage-uniforms/<int:pk>/images', views.UniformImages.as_view()),
]