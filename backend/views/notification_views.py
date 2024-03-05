from django.contrib import messages

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.permissions import IsAdminOrReadOnly
from backend.serializers import NotificationSerializer
from backend.models import Notification

__all__ = ['NotificationList']

class NotificationList(ListAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Notification.objects.all().order_by('-status', '-modified_at')
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": {
                "count": len(response.data),
                "rows": response.data
            }
        })
