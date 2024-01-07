from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.models import Payment

from . extras import CustomModelSerializer

__all__ = ['PaymentSerializer', ]

class PaymentSerializer(CustomModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        
               
    
    


