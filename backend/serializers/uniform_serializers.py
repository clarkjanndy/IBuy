from django.db.models import F
from rest_framework import serializers

from backend.models import Category, Uniform, Inventory, UniformImage

from . extras import CustomModelSerializer

__all__ = ['CategorySerializer', 'UniformSerializer', 'UniformImageSerializer']

class CategorySerializer(CustomModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class UniformSerializer(CustomModelSerializer):
    quantity = serializers.IntegerField(source='inventory.quantity')
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image = serializers.SerializerMethodField()
    image = serializers.ImageField(required = False)

    class Meta:
        model = Uniform
        exclude = ('created_by', 'modified_by')
        
    def get_main_image(self, instance):
        return instance.main_image

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs.get('quantity', 0) < 0:
            raise serializers.ValidationError({'quantity': 'Must be a postive number.'})
        
        if not isinstance(attrs.get('available_sizes'), list):
            raise serializers.ValidationError({'available_sizes': 'Please supply a valid list.'})
        
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
    
        # pop data that are not needed in create
        inventory = validated_data.pop('inventory')
        # pop image do not include in create
        image = validated_data.pop('image')
       
        # append current user data
        validated_data.update({'created_by': user})
        validated_data.update({'modified_by': user})
        uniform = super().create(validated_data)
        
        # create inventory instance
        Inventory.objects.create(uniform = uniform, quantity = inventory.get('quantity'))
        
        # create uniform image instance
        UniformImage.objects.create(uniform=uniform, image=image)
        
        return uniform

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        
        # pop data that are not needed in update
        inventory = validated_data.pop('inventory')
         # pop image do not include in create
        image = validated_data.pop('image')
       
        validated_data.update({'modified_by': user})
        uniform = super().update(instance, validated_data)

        # update inventory instance
        Inventory.objects.filter(uniform = uniform).update(quantity = F('quantity') + inventory.get('quantity'))
        return uniform
    
class UniformImageSerializer(CustomModelSerializer):
    
    class Meta:
        model = UniformImage
        fields = ('id','image', )
   

   
    