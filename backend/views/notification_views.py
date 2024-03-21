from django.contrib import messages

from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.exceptions import ClientError

from backend.permissions import IsAdminOrReadOnly
from backend.serializers import NotificationSerializer
from backend.models import Notification

__all__ = ['NotificationList', 'NotificationMarkRead', 'NotificationMarkReadAll']

class NotificationList(ListAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Notification.objects.all().order_by('-status', '-modified_at')
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)
    
    def get(self, request, *args, **kwargs):
        # get all notifs first
        unseen = self.get_queryset().filter(status='unseen')
        count = unseen.count()
        
        # get only the first 5 notifs
        query_set = self.get_queryset()[:5]
        serializer = self.serializer_class(query_set, many=True)
        
        return Response({
            "status": "success", 
            "data": {
                "count": count,
                "rows": serializer.data
            }
        })
        
class NotificationMarkRead(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Notification.objects.all().order_by('-status', '-modified_at')
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        request = self.request
        return super().get_queryset().filter(user = request.user)
    
    def get_object(self):
        request = self.request
        try:
            notif_id = self.kwargs.get('pk')
            obj = self.get_queryset().get(id=notif_id)
        except Notification.DoesNotExist:
            raise ClientError({"message": "Not found"}, 404)
        
        return obj
        
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'seen'
        instance.save()
        
        serializer = self.get_serializer(instance)
        
        return Response({
            "status": "success", 
            "data": serializer.data
        })
        
class NotificationMarkReadAll(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Notification.objects.all().order_by('-status', '-modified_at')
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        request = self.request
        return super().get_queryset().filter(user = request.user, status='unseen')
        
    def post(self, request, *args, **kwargs):
        self.get_queryset().update(status='seen')
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "status": "success", 
            "data": serializer.data
        })

            
