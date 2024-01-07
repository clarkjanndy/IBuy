import secrets
import string

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
    amount = models.DecimalField(max_digits=8, decimal_places=2, default = 0)
    status = models.CharField(choices=STATUS, default='pending', max_length=12)
    receipt_image = models.ImageField(upload_to='payment-receipts/', null=True, blank=True)
                
    def __str__(self):
        return self.ref_no
    
class PaymentOption(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    payment_instruction = models.TextField()

    def __str__(self) -> str:
        return self.name