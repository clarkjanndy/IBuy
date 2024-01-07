from django.contrib import messages

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Payment
from backend.serializers import PaymentSerializer, BuyNowSerializer
from backend.exceptions import ClientError, SerializerValidationError
from backend.services.order_service import OrderService

__all__ = ['PaymentCreate', ]

class PaymentCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Payment.objects.prefetch_related('user', 'order')
    serializer_class = PaymentSerializer
    
       

    
    
    
        