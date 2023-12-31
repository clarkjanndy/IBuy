from django.db import models
from django.utils import timezone
from . extras import TimeStampedModel

__all__ = ['Cart']

def default_expiration_date():
    return timezone.now() + timezone.timedelta(days=7)

class Cart(TimeStampedModel):
    STATUS = (
        ('on-cart', 'On-Cart'),
        ('purchased', 'Purchased'),
        ('deleted', 'Deleted')
    )
    
    uniform = models.ForeignKey('Uniform', related_name='on_cart_items', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='cart_items', on_delete=models.CASCADE)
    variant = models.CharField(max_length=100)
    expiry_date = models.DateTimeField(default=default_expiration_date)
    quantity = models.PositiveIntegerField(default = 1)
    status = models.CharField(choices=STATUS, default='on-cart', max_length=12)
    
    def delete(self, *args, **kwargs):
        self.status = 'deleted'
        self.save()
        
        #update quantity of the selected uniform
        uniform = self.uniform
        inventory = uniform.inventory
        inventory.quantity += self.quantity
        inventory.save()
                
    def __str__(self) -> str:
        return self.uniform.name
    
    @property
    def total_price(self):
        return self.uniform.price * self.quantity

    
   