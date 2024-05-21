from django.conf import settings
from django.db import models
from django.db.models import Sum
from . extras import TimeStampedModel

from . user import User, Department
from . order import OrderItem
__all__ = ['Category','Uniform', 'Variant', 'UniformImage']

class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'
    
class Uniform(TimeStampedModel):

    STATUSES = (
        ('in-stock', 'In-Stock'),
        ('out-of-stock', 'Out-of-Stock'),
        ('draft', 'Draft')
    )
    
    UNITS = (
        ('piece', 'Piece'),
        ('meter', 'Meter')
    )
    
    department = models.ForeignKey(Department, related_name='uniforms', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=15, choices=UNITS, default='piece')
    category = models.ForeignKey(Category, related_name='uniforms', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUSES, default='in-stock')
    created_by = models.ForeignKey(User, related_name='created_uniforms', on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, related_name='modified_uniforms', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def sold(self):
        order = OrderItem.objects.select_related('payment').filter(uniform=self, order__payment__status='approved').aggregate(quantity=Sum('quantity'))        
        return order.get('quantity') or 0
    
    @property
    def quantity(self):
        variants = self.variants.all().aggregate(quantity = Sum('quantity'))
        return variants['quantity'] or 0
    
    @property
    def is_allowed_non_whole_quantity(self):
        # allow non_whole only on meters
        return self.unit == 'meter'        
                        
    @property
    def is_active(self):
        return True if self.status == 'in-stock' else False
    
    @property
    def uniform_images(self):
        return UniformImage.objects.filter(uniform=self).order_by('-created_at')
    
    @property
    def main_image(self):
        instance = UniformImage.objects.filter(uniform=self).order_by('-created_at').first()
        if instance:
            return instance.image.url if hasattr(instance.image, 'url') else self.default_photo_url        
        return self.default_photo_url
    
    @property
    def default_photo_url(self):        
        return f"{settings.STATIC_URL}frontend/img/no-image.png"
    
class Variant(TimeStampedModel):            
    uniform = models.ForeignKey(Uniform, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='DEFAULT')
    quantity = models.DecimalField(max_digits=8, decimal_places=2)    
    
    def __str__(self) -> str:
        return f"{self.uniform} - {self.name}"
    
class UniformImage(TimeStampedModel):
    uniform = models.ForeignKey(Uniform, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uniform-images/')

    def __str__(self) -> str:
        return self.image.url