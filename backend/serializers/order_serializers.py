from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.models import Order, PaymentOption, Uniform

from . extras import CustomModelSerializer, CustomSerializer

__all__ = ['OrderSerializer', 'PlaceOrderSerializer', 'BuyNowSerializer']

class OrderSerializer(CustomModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', )
        
class PlaceOrderSerializer(CustomSerializer):
    cart_id = serializers.JSONField()
    payment_option = serializers.PrimaryKeyRelatedField(queryset=PaymentOption.objects.all())
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        if not attrs['cart_id']:
            raise ValidationError({"cart_id": 'This field cannot be an empty list.'})
        
        if not type(attrs['cart_id']) == list:
            raise ValidationError({"cart_id": 'Must be a list.'})
            
        return attrs
    
class BuyNowSerializer(CustomSerializer):
    uniform = serializers.PrimaryKeyRelatedField(queryset=Uniform.objects.select_related('inventory').filter(status = 'active'))
    payment_option = serializers.PrimaryKeyRelatedField(queryset=PaymentOption.objects.all())
    quantity = serializers.IntegerField()
    variant = serializers.CharField()
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        uniform = attrs['uniform']
        variant = attrs['variant']
        quantity = attrs['quantity']
        
        if uniform.inventory.quantity < 1 or uniform.inventory.quantity < quantity:
            raise ValidationError({'quantity': "Maximum quantity reached."})
        
        if not variant in uniform.available_sizes:
            raise serializers.ValidationError({"varaint": "Invalid variant."})
        
        return attrs
        
               
    
    


