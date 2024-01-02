from django.db import models
from . extras import TimeStampedModel

__all__ = ['PaymentOption']

class PaymentOption(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    payment_instruction = models.TextField()

    def __str__(self) -> str:
        return self.name