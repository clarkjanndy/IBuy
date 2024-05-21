from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.models import Order, PaymentOption, Uniform, OrderHistory, Variant

from . extras import CustomModelSerializer, CustomSerializer
from backend.utils.extras import is_fractional_part_zero

__all__ = ['OrderSerializer', 'OrderHistorySerializer', 'PlaceOrderSerializer', 'BuyNowSerializer']

class OrderSerializer(CustomModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', )

class OrderHistorySerializer(CustomModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'
        read_only_fields = ('modified_by', )
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({'modified_by': request.user})
        
        return super().create(validated_data)
        
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
    uniform = serializers.PrimaryKeyRelatedField(queryset=Uniform.objects.filter(status = 'in-stock'))
    payment_option = serializers.PrimaryKeyRelatedField(queryset=PaymentOption.objects.all())
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    variant = serializers.CharField(allow_null=True, allow_blank=True)
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        uniform = attrs.get('uniform')
        variant = attrs.get('variant')
        quantity = attrs.get('quantity')
        
        if quantity > 10:
            raise serializers.ValidationError({"quantity": "You are limited to buy 10 items only."})
        
        variant = uniform.variants.filter(name = variant).first()        
        if not variant:
            raise serializers.ValidationError({"varaint": "Invalid variant."})
            
        if variant.quantity < 1 or variant.quantity < quantity:
            raise ValidationError({'quantity': "Maximum quantity reached."})
        
        if not is_fractional_part_zero(quantity) and not uniform.is_allowed_non_whole_quantity:
            raise ValidationError({"quantity": "Invalid quantity. Please input a whole number."})
           
        return attrs
        
               
    
    


