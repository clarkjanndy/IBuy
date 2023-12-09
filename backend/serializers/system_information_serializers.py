from . extras import CustomModelSerializer
from backend.models import SystemInformation

__all__ = ['SystemInformationSerializer']

class SystemInformationSerializer(CustomModelSerializer):
    class Meta:
        model = SystemInformation
        fields = '__all__'