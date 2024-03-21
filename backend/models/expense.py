from django.db import models
from .extras import TimeStampedModel

__all__ = ['Expense']

class Expense(TimeStampedModel):
    
    KIND = (
        ('cost', 'Cost'),
        ('material', 'Material')
    )
        
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=20, choices=KIND, default='cost')
    billing_month = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    remarks = models.TextField()
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='expenses_created')
    modified_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='expenses_modified')

    def __str__(self) -> str:
        return self.name