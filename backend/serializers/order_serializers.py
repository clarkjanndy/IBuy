from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.models import Order, PaymentOption

from . extras import CustomModelSerializer, CustomSerializer

__all__ = ['OrderSerializer', 'PlaceOrderSerializer']

class OrderSerializer(CustomModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', )
        
class PlaceOrderSerializer(CustomSerializer):
    cart_id = serializers.JSONField()
    payment_option = serializers.IntegerField()
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        if not attrs['cart_id']:
            raise ValidationError({"cart_id": 'This field cannot be an empty list.'})
        
        if not type(attrs['cart_id']) == list:
            raise ValidationError({"cart_id": 'Must be a list.'})
        
        payment_option = PaymentOption.objects.filter(pk = attrs['payment_option'])
        if not payment_option.exists():
            raise ValidationError({"payment_option": 'Invalid payment option.'})
            
        return attrs


