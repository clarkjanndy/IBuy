import secrets
import string

from django.conf import settings
from django.db import models
from . extras import TimeStampedModel

__all__ = ['Payment', 'PaymentOption']

def generate_reference_number():
    # Generate an 8-character reference number with uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))

STATUS = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('declined', 'Declined')
)

class Payment(TimeStampedModel):
    ref_no = models.CharField(max_length=10, default=generate_reference_number, editable=False, unique=True, primary_key=True)
    order = models.OneToOneField('Order', related_name='payment', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(choices=STATUS, default='pending', max_length=12)
    receipt_image = models.ImageField(upload_to='payment-receipts/', null=True, blank=True)
                
    def __str__(self):
        return self.ref_no
    
    @property
    def receipt_image_url(self):
        if self.receipt_image:
            return self.receipt_image.url if hasattr(self.receipt_image, 'url') else self.default_photo_url
        
        return self.default_photo_url
    
    @property
    def default_photo_url(self):        
        return f"{settings.STATIC_URL}frontend/img/no-image.png"
    
class PaymentOption(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    payment_instruction = models.TextField()
    is_facilitated = models.BooleanField(default=False)
    receipt_required = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name