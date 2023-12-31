from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.serializers import CartSerializer
from backend.models import Cart
from backend.exceptions import ClientError

__all__ = ['CartListCreate', 'CartById']

class CartListCreate(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()
        return queryset.filter(user=request.user, status='on-cart')

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
        
class CartById(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()
        return queryset.filter(user = request.user, status='on-cart')
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = 'Cart item deleted successfully!'
        
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })