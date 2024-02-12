from django.db.models import F
from django.db.models import Sum
from rest_framework import serializers

from . extras import CustomModelSerializer
from backend.models import Cart, Inventory

__all__ = ['CartSerializer']

class CartSerializer(CustomModelSerializer):
    total_price = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    uniform_image = serializers.SerializerMethodField()
    uniform_name = serializers.SerializerMethodField()
   
    class Meta:
        model = Cart
        exclude = ('user', )
    
    def get_unit(self, instance):
        return instance.uniform.inventory.unit
        
    def get_unit_price(self, instance):
        return instance.uniform.price
        
    def get_total_price(self, instance):
        return instance.total_price
    
    def get_uniform_image(self, instance):
        return instance.uniform.main_image
    
    def get_uniform_name(self, instance):
        return instance.uniform.name
        
    def validate(self, attrs):
        request = self.context.get('request')
        attrs = super().validate(attrs)
        uniform = attrs['uniform']
        
        if uniform.variants and not attrs['variant'] in uniform.variants:
            raise serializers.ValidationError({"variant": "Invalid variant."})

        if uniform.inventory.quantity < attrs['quantity']:
            raise serializers.ValidationError({"quantity": "Maximum quantity reached."})
        
        if attrs['quantity'] > 10:
            raise serializers.ValidationError({"quantity": "Adding to cart is only limited to 10 items only."})
            
        on_cart_quantity = Cart.objects.filter(user=request.user, status='on-cart').aggregate(Sum('quantity'))['quantity__sum']
        if on_cart_quantity and (on_cart_quantity + attrs['quantity']) > 10:
            raise serializers.ValidationError({"quantity": "Adding to cart is only limited to 10 items only."})
    
        return attrs
        
    def create(self, validated_data):
        request = self.context.get('request')   
        user = request.user
        
        # append current user data
        validated_data.update({"user": user})
        cart_item, created = Cart.objects.get_or_create(
            status='on-cart',
            user=validated_data['user'],
            uniform=validated_data['uniform'],
            variant=validated_data['variant'],
            defaults = validated_data
        )
        
        if not created:
            cart_item.quantity += validated_data['quantity']
            cart_item.save()
        
        # update the quantity of the uniform after successfully adding to cart
        uniform = cart_item.uniform
        Inventory.objects.filter(uniform = uniform).update(quantity = F('quantity') - validated_data['quantity'])
        
        return cart_item