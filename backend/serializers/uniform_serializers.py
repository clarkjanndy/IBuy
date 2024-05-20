from decimal import Decimal

from django.db.models import F
from rest_framework import serializers

from backend.models import Category, Uniform, UniformImage, Variant
from backend.utils.extras import has_duplicates

from . extras import CustomModelSerializer


__all__ = ['CategorySerializer', 'UniformSerializer', 'UniformImageSerializer']

class CategorySerializer(CustomModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class VariantSerializer(CustomModelSerializer):
    class Meta:
        model = Variant
        fields = ("name", "quantity")

class UniformSerializer(CustomModelSerializer):
    # quantity = serializers.IntegerField(source='inventory.quantity')
    # unit = serializers.CharField(source='inventory.unit')
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image = serializers.SerializerMethodField()
    image = serializers.ImageField(required = False)
    variant_list = serializers.JSONField(write_only=True)

    class Meta:
        model = Uniform
        exclude = ('created_by', 'modified_by')
        
    def get_main_image(self, instance):
        return instance.main_image
    
    def get__variants(self, instance):
        return {}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        if not isinstance(attrs.get('variant_list'), list):
            raise serializers.ValidationError({'variants': 'Please supply a valid list.'})
        
        if attrs.get('department') and attrs.get('category').name == 'Universal':
            raise serializers.ValidationError({'department': 'Keep this field blank for Universal categories.'})
        
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # pop image do not include in create
        image = validated_data.pop('image')
        variant_list = validated_data.pop('variant_list')
       
        # append current user data
        validated_data.update({'created_by': user})
        validated_data.update({'modified_by': user})
        print(validated_data)
        uniform = super().create(validated_data)
        
        # create or update each variant
        variant_list = [variant for variant in variant_list if variant['name'] and variant['quantity']]
        for variant in variant_list:
            variant_obj, created = Variant.objects.get_or_create(uniform=uniform, name=variant['name'].upper(),
                defaults = {"quantity": variant['quantity']}
            )
            if not created:
                variant_obj.quantity = variant_obj.quantity + Decimal(variant['quantity'])
                variant_obj.save()
            
        # create uniform image instance 
        UniformImage.objects.create(uniform=uniform, image=image)
        
        return uniform

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        
        # pop data that are not needed in update
        variant_list = validated_data.pop('variant_list')
       
        validated_data.update({'modified_by': user})
        uniform = super().update(instance, validated_data)

        # create or update each variant
        variant_list = [variant for variant in variant_list if variant['name'] and variant['quantity']]
        for variant in variant_list:
            variant_obj, created = Variant.objects.get_or_create(uniform=uniform, name=variant['name'].upper(),
                defaults = {"quantity": variant['quantity'] }
            )
            if not created:
                variant_obj.quantity = Decimal(variant['quantity'])
                variant_obj.save()
        
        return uniform
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)   
        
        # get all variants associated to the uniform
        variants = Variant.objects.filter(uniform__id = representation['id'])
        serializer = VariantSerializer(variants, many=True)
        representation['variant_list'] = serializer.data
                
        return representation

 
class UniformImageSerializer(CustomModelSerializer):
    
    class Meta:
        model = UniformImage
        fields = ('id','image', )
   

   
    