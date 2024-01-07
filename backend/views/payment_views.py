from django.contrib import messages

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Payment
from backend.serializers import PaymentSerializer

__all__ = ['PaymentCreate', ]

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
       

    
    
    
        