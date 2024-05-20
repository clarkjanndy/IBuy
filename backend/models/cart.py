from django.db import models
from django.db.models import F
from django.utils import timezone
from . extras import TimeStampedModel
from . uniform import Variant

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
    variant = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.DateTimeField(default=default_expiration_date)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(choices=STATUS, default='on-cart', max_length=12)
    
    def delete(self, *args, **kwargs):
        self.status = 'deleted'
        self.save()
        
        # update quantity of the selected variant
        uniform = self.uniform
        Variant.objects.filter(uniform = uniform, name = self.variant).update(quantity = F('quantity') + self.quantity)
        
    def __str__(self) -> str:
        return self.uniform.name
    
    @property
    def total_price(self):
        return self.uniform.price * self.quantity

    
   