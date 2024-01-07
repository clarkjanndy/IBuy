from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.models import Payment
from backend.services.order_service import OrderService

from . extras import CustomModelSerializer

__all__ = ['PaymentSerializer', ]

class PaymentSerializer(CustomModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', )
        
    def validate(self, attrs):
        attrs = super().validate(attrs)
        amount = attrs['amount']
        order = attrs['order']
        request = self.context.get('request')
        
        if amount < order.total:
            raise ValidationError({'amount': 'Amount must be greater than or equal to order total.'})
        
        if not request.user.is_superuser and not order.user == request.user:
            raise ValidationError({'order': 'You are unable to pay this.'})
        
        return attrs
        
    def create(self, validated_data):
        request = self.context.get('request')
        
        # payment of normal users is defaulted to pending
        if not request.user.is_superuser:
            validated_data.update({"status": "pending"})
            
        order = validated_data['order']
        # create history 
        service = OrderService(order)
        service.create_history(request.user, f'Order paid via {order.payment_option}', 'to-ship')
                
        return super().create(validated_data)
        
    def save(self, **kwargs):
        validated_data = self.validated_data
        # asign order user as user of the payment
        order = validated_data['order']
        validated_data.update({'user': order.user})
        return super().save(**kwargs)
        
               
    
    


