from rest_framework.serializers import ValidationError

from backend.models import Expense
from .extras import CustomModelSerializer

__all__ = ['ExpenseSerializer']

class ExpenseSerializer(CustomModelSerializer):

    class Meta:
        model = Expense
        exclude = ('created_by', 'modified_by')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        
        validated_data['created_by'] =  user   
        validated_data['modified_by'] =  user       
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        
        validated_data['modified_by'] =  user         
        return super().update(instance, validated_data)