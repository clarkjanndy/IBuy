from django.contrib import messages

from rest_framework.generics import GenericAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from backend.models import Order, OrderItem, Cart, OrderHistory
from backend.serializers import PlaceOrderSerializer, OrderHistorySerializer, BuyNowSerializer, OrderSerializer
from backend.exceptions import ClientError, SerializerValidationError
from backend.services.order_service import OrderService

__all__ = ['PlaceOrder', 'BuyNow', 'OrderDetail', 'OrderHistoryCreate']

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
                
            # call service to do necessary things
            service = OrderService(order)
            service.post_order_placement_process(user=request.user)
        
            return Response({
                "status": "success", 
                "data": {
                    "message": f'Your order with reference number {order.ref_no} has been succesfully placed.',
                    "ref_no": order.ref_no
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
            
            uniform = validated_data.get('uniform')
            variant = validated_data.get('variant')
            quantity = validated_data.get('quantity')
            
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
            
            # call service to do necessary things
            service = OrderService(order)
            service.post_order_placement_process(user=request.user)
      
            return Response({
                "status": "success", 
                "data": {
                    "message": f'Your order with reference number {order.ref_no} has been succesfully placed.',
                    "ref_no": order.ref_no
                }
            })
            
        except SerializerValidationError as err:
            raise err
        
        except ClientError as err:
            raise err

class OrderDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'ref_no'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data = response.data
        
        return Response({
            "status": "success", 
            "data": data
        })

class OrderHistoryCreate(CreateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        
        messages.success(request, f"Order {data.get('order')} succesfully updated.")
        return Response({
            "status": "success", 
            "data": data
        })

    
    
        