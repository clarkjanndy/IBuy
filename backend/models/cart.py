from django.db import models
from django.utils import timezone
from . extras import TimeStampedModel

__all__ = ['Cart']

def default_expiration_date():
    return timezone.now() + timezone.timedelta(days=7)

class Cart(TimeStampedModel):
    uniform = models.ForeignKey('Uniform', related_name='on_cart_items', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='cart_items', on_delete=models.CASCADE)
    variant = models.CharField(max_length=100)
    expiry_date = models.DateTimeField(default=default_expiration_date)
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self) -> str:
        return self.uniform.name
    
    @property
    def total_price(self):
        return self.uniform.price * self.quantity

    
   