from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Order, OrderItem, Cart
from backend.serializers import PlaceOrderSerializer, CartSerializer
from backend.exceptions import ClientError, SerializerValidationError

__all__ = ['PlaceOrder']

class PlaceOrder(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PlaceOrderSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid()
            validated_data = serializer.validated_data
            
            cart_items = Cart.objects.select_related('uniform').filter(
                id__in = validated_data['cart_id'],
                user = request.user,
                status = 'on-cart'
            )  
            
            if not cart_items.exists():
                raise ClientError({"message": "No cart item found."})
            
            # create the Order
            order = Order.objects.create(
                user_id = request.user.pk,
                payment_option_id = validated_data['payment_option'],
            )
            # create the OrderItem(s)
            for cart in cart_items:
                OrderItem.objects.create(
                    order = order,
                    uniform = cart.uniform,
                    variant = cart.variant,
                    unit_price = cart.uniform.price,
                    quantity = cart.quantity,
                )
                cart.status = 'purchased'
                cart.save()
            
            messages.success(request, message := f'Your order with reference number {order.ref_no} has been succesfully placed.')          
            return Response({
                "sucess": True,
                "data": {
                    "message": message
                }
            })
            
        except SerializerValidationError as err:
            raise err
        
        except ClientError as err:
            raise err
    
        