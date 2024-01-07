from django.contrib import messages

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.models import Payment
from backend.serializers import PaymentSerializer

__all__ = ['PaymentCreate', 'PaymentById' ]

class PaymentCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Payment.objects.prefetch_related('user', 'order')
    serializer_class = PaymentSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        
        # messages.success(request, f"Category {data.get('name')} created successfully!")
        return Response({
            "status": "success", 
            "data": data
        })
        
class PaymentById(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Payment.objects.prefetch_related('user', 'order')
    serializer_class = PaymentSerializer
    lookup_field = 'ref_no'
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        data = response.data
        
        messages.success(request, f"Payment succesfully {data.get('status')}.")
        return Response({
            "status": "success", 
            "data": data
        })
        
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data = response.data
        
        return Response({
            "status": "success", 
            "data": data
        })
       

    
    
    
        