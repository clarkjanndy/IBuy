from django.db import models
from .extras import TimeStampedModel

__all__ = ['Expense']

class Expense(TimeStampedModel):
    
    KIND = (
        ('cost', 'Cost'),
        ('material', 'Material')
    )
    
    CAPITAL_TYPE = (
        ('cloth_capital', 'Cloth Capital'),
        ('departmental_uniform_capital', 'Departmental Uniform Capital')
    )
        
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=20, choices=KIND, default='cost')
    capital_type = models.CharField(max_length=50, choices=CAPITAL_TYPE, blank=True, null=True)
    billing_date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    remarks = models.TextField()
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='expenses_created')
    modified_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='expenses_modified')

    def __str__(self) -> str:
        return self.name
   
    @classmethod
    def capital_type_mapping(cls):
        mapping = {}
        for item in cls.CAPITAL_TYPE:
            mapping[item[0]] = item[1]  
            
        return mapping          