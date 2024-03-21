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
    path('buy-now', views.BuyNow.as_view()),
    path('orders/<str:ref_no>', views.OrderDetail.as_view()),    
    path('order-histories', views.OrderHistoryCreate.as_view()),    
        
    #Payment
    path('payments', views.PaymentCreate.as_view()),
    path('payments/<str:ref_no>', views.PaymentById.as_view()),
    
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

    # Expense
    path('expenses', views.ExpenseListCreate.as_view()),
    path('expenses/<int:pk>', views.ExpenseById.as_view()),
    
    # Notification
    path('notifications', views.NotificationList.as_view()),
    path('notifications/<int:pk>/mark-as-read', views.NotificationMarkRead.as_view()),
    path('notifications/mark-as-read-all', views.NotificationMarkReadAll.as_view()),
    
    # Notification
    path('report-pdf', views.ReportPDF.as_view()),
]
