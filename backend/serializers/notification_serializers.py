from . extras import CustomModelSerializer
from backend.models import Notification

__all__ = ['NotificationSerializer']

class NotificationSerializer(CustomModelSerializer):
    class Meta:
        model = Notification
        exclude = ('user', )