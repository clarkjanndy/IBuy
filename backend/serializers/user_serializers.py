from django.contrib.auth.hashers import make_password

from rest_framework.serializers import ValidationError

from backend.models import User
from .extras import CustomModelSerializer

__all__ = ['UserSerializer']

class UserSerializer(CustomModelSerializer):

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'last_login', 'is_active', 'groups', 'user_permissions', 'password')
        read_only_fields = ('date_joined', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs.get('role') == 'student' and not attrs.get('student_id'):
            raise ValidationError({'student_id': 'This field is required.'})
        
        # ignore photo if null or a Falsy value is passed
        if 'photo' in attrs and not attrs.get('photo'):
            attrs.pop('photo')
        
        return attrs

    def create(self, validated_data):
        # set the username as password and the hash
        hashed_password = make_password(validated_data['username'])
        validated_data.update({"password": hashed_password})
        
        # set superuser and is_staff flag to true if role is admin
        if validated_data['role'] == 'admin':
            validated_data['is_superuser'] = True
            validated_data['is_staff'] = True
                
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # set superuser and is_staff flag to true if role is admin
        if validated_data['role'] == 'admin':
            validated_data['is_superuser'] = True
            validated_data['is_staff'] = True

        else:
            validated_data['is_superuser'] = False
            validated_data['is_staff'] = False
            
        
        return super().update(instance, validated_data)