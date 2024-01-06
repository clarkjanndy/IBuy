from django.urls import path
from backend import views

urlpatterns = [
    # Auth
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('register', views.RegistrationView.as_view()),
    path('change-password', views.ChangePasswordView.as_view()),

    # Profile
    path('profile', views.UserMyProfile.as_view()),
    
    # Cart
    path('carts', views.CartListCreate.as_view()),
    path('carts/<int:pk>', views.CartById.as_view()),
    
    #Order
     path('place-order', views.PlaceOrder.as_view()),
    
    # Users
    path('users', views.UserListCreate.as_view()),
    path('users/<int:pk>', views.UserById.as_view()),
    path('users/<int:pk>/activate-or-deactivate', views.UserActivateDeactivate.as_view()),

    # FAQ
    path('faqs', views.FAQListCreate.as_view()),
    path('faqs/<int:pk>', views.FAQById.as_view()),

    # System Information
    path('system-informations', views.SystemInformationListCreate.as_view()),
    path('system-informations/<int:pk>', views.SystemInformationById.as_view()),

    # Uniforms
    path('categories', views.CategoryListCreate.as_view()),
    path('categories/<int:pk>', views.CategoryById.as_view()),
    path('uniforms', views.UniformListCreate.as_view()),
    path('uniforms/<int:pk>', views.UniformById.as_view()),
    path('uniforms/<int:pk>/images', views.UniformImageListCreate.as_view()),
    path('uniforms/<int:uniform_pk>/images/<int:pk>', views.UniformImageById.as_view()),

]
