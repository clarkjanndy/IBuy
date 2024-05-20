import secrets
import string

from django.db import models
from . extras import TimeStampedModel
from . notification import Notification


__all__ = ['Order', 'OrderItem', 'OrderHistory']

def generate_reference_number():
    # Generate an 8-character reference number with uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))

STATUS = (
    ('to-pay', 'To Pay'),
    ('to-prepare', 'To Prepare'),
    ('to-recieve', 'To Recieve'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)

class Order(TimeStampedModel):
    ref_no = models.CharField(max_length=10, default=generate_reference_number, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey('User', related_name='orders', on_delete=models.CASCADE)
    payment_option =  models.ForeignKey('PaymentOption', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2, default = 0)
    status = models.CharField(choices=STATUS, default='to-pay', max_length=12)
                
    def __str__(self):
        return self.ref_no
    
    @property
    def is_payable(self):
        return self.status == 'to-pay'
    
    @property
    def has_payment(self):
        return hasattr(self, 'payment')
    
class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items')
    uniform = models.ForeignKey('Uniform', on_delete=models.CASCADE, related_name='order_item')
    variant = models.CharField(max_length=100, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.order.ref_no
    
    def save(self, *args, **kwargs):
        # calculate subtotal
        self.subtotal = self.unit_price * self.quantity
        
        # update the total of the order
        order = self.order
        order.total += self.subtotal
        order.save()
        super().save( *args, **kwargs)
    
class OrderHistory(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    remarks = models.TextField()
    status = models.CharField(choices=STATUS, default='to-pay', max_length=12)
    modified_by = models.ForeignKey('User', related_name='modified_order_history', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-modified_at', )
    
    def __str__(self):
        return self.remarks
    
    def save(self, *args, **kwargs):
        order = self.order
        # update the status of the order if there are changes in the history status
        if not order.status == self.status:
            order.status = self.status
            order.save()     
            self.notify_user_order_status_changes()
            
        super().save( *args, **kwargs)
    
    def notify_user_order_status_changes(self):
        level_map = {
            'to-pay': 'primary',
            'to-prepare': 'primary',
            'to-recieve': 'primary',
            'completed': 'success',
            'cancelled': 'danger'
        }
        
        content = f'Your order with reference number {self.order.ref_no} is now in the {self.get_status_display()} status.'
        Notification.objects.create(
            user = self.order.user,
            level = level_map.get(self.status),
            content = content,
            link = f'/my-orders/{self.order.ref_no}'
        )
        
        print(f'User has been notified about order status change of order {self.order.ref_no}.')
        
    
    
  
    

    
   