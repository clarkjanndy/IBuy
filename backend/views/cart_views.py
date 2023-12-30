from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.permissions import IsAdminOrReadOnly
from backend.serializers import CartSerializer
from backend.models import Cart

__all__ = ['CartListCreate']

class CartListCreate(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()
        return queryset.filter(user = request.user)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })