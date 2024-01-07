from collections.abc import Iterable
import secrets
import string

from django.db import models
from . extras import TimeStampedModel

__all__ = ['Order', 'OrderItem', 'OrderHistory']

def generate_reference_number():
    # Generate an 8-character reference number with uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))

STATUS = (
    ('to-pay', 'To Pay'),
    ('to-ship', 'To Ship'),
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
    
class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items')
    uniform = models.ForeignKey('Uniform', on_delete=models.CASCADE)
    variant = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
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
    
    def save(self, *args, **kwargs):
        order = self.order
        # update the status of the order if there are changes in the history status
        if not order.status == self.status:
            order.status = self.status
            order.save()
            
        super().save( *args, **kwargs)
    
    def __str__(self):
        return self.remarks
    
    class Meta:
        ordering = ('-modified_at', )
    

    
   