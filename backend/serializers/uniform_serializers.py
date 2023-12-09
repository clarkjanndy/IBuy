from django.db.models import F
from rest_framework import serializers

from backend.models import Category, Uniform, Inventory, UniformImage
from . extras import CustomModelSerializer, CustomSerializer

__all__ = ['CategorySerializer', 'UniformSerializer', 'UniformImageSerializer']

class CategorySerializer(CustomModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UniformSerializer(CustomModelSerializer):
    quantity = serializers.IntegerField(write_only=True)
    VALID_SIZES = ['EXTRA SMALL', 'SMALL', 'MEDIUM', 'LARGE', 'EXTRA LARGE']

    class Meta:
        model = Uniform
        exclude = ('created_by', 'modified_by')

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs.get('quantity', 0) < 0:
            raise serializers.ValidationError({'quantity': 'Must be a postive number.'})
        
        if not set(attrs.get('available_sizes', [])).issubset(self.VALID_SIZES):
            raise serializers.ValidationError({'available_sizes': 'Field must not contain invalid sizes.'})
        
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # pop quantity do not include in create
        quantity = validated_data.pop('quantity')
        # append current user data
        validated_data.update({'created_by': user})
        validated_data.update({'modified_by': user})
        uniform = super().create(validated_data)

        # create inventory instance
        Inventory.objects.create(uniform = uniform, quantity = quantity)
        return uniform

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        
        # pop quantity do not include in create
        quantity = validated_data.pop('quantity')
        validated_data.update({'modified_by': user})
        uniform = super().update(instance, validated_data)

        # update inventory instance
        Inventory.objects.filter(uniform = uniform).update(quantity = F('quantity') + quantity)
        return uniform

    def to_representation(self, instance):
        instance = super().to_representation(instance)

        inventory = Inventory.objects.filter(pk = instance.get('id')).first()
        instance.update({'quantity': inventory.quantity if inventory else None})

        category = Category.objects.filter(pk = instance.get('category')).first()
        instance.update({'category': category.name if category else None})
        
        return instance
    
class UniformImageSerializer(CustomModelSerializer):
    
    class Meta:
        model = UniformImage
        fields = ('id','image', )
   

   
    