from django.contrib import messages

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Order, OrderItem, Cart, Uniform
from backend.serializers import PlaceOrderSerializer, BuyNowSerializer
from backend.exceptions import ClientError, SerializerValidationError

__all__ = ['PlaceOrder', 'BuyNow']

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
                user = request.user,
                payment_option = validated_data['payment_option'],
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

class BuyNow(GenericAPIView):    
    permission_classes = (IsAuthenticated, )
    serializer_class = BuyNowSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid()
            validated_data = serializer.validated_data
            
            # create the Order
            order = Order.objects.create(
                user = request.user,
                payment_option = validated_data['payment_option'],
            )
            
            uniform = validated_data['uniform']
            variant = validated_data['variant']
            quantity = validated_data['quantity']
            
            # create the OrderItem
            OrderItem.objects.create(
                order = order,
                uniform = uniform,
                variant = variant,
                unit_price = uniform.price,
                quantity = quantity,
            )
            
            #update inventory
            inventory = uniform.inventory
            inventory.quantity -= quantity
            inventory.save()
            
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
        
    
    
        