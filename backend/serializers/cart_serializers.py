from django.db.models import F
from rest_framework import serializers

from . extras import CustomModelSerializer
from backend.models import Cart, Inventory

__all__ = ['CartSerializer']

class CartSerializer(CustomModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ('user', )
        
    def get_total_price(self, instance):
        return instance.total_price
        
    def validate(self, attrs):
        attrs = super().validate(attrs)
        uniform = attrs['uniform']
        
        if not attrs['variant'] in uniform.available_sizes:
            raise serializers.ValidationError({"varaint": "Invalid variant."})

        if uniform.inventory.quantity < attrs['quantity']:
            raise serializers.ValidationError({"quantity": "Maximum quantity reached."})
        
        return attrs
        
    def create(self, validated_data):
        request = self.context.get('request')   
        user = request.user
        
        # append current user data
        validated_data.update({"user": user})
        cart_item = super().create(validated_data)
        
        # update the quantity of the uniform after successfully adding to cart
        uniform = cart_item.uniform
        Inventory.objects.filter(uniform = uniform).update(quantity = F('quantity') - cart_item.quantity)
        
        return cart_item