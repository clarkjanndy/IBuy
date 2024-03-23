from django.conf import settings
from django.db import models
from django.db.models import Sum
from . extras import TimeStampedModel

from . user import User, Department
from . order import OrderItem
__all__ = ['Category','Uniform', 'UniformImage', 'Inventory']

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
    
    department = models.ForeignKey(Department, related_name='uniforms', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='uniforms', on_delete=models.CASCADE)
    variants = models.JSONField(default=list)
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
    
    
class UniformImage(TimeStampedModel):
    uniform = models.ForeignKey(Uniform, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uniform-images/')

    def __str__(self) -> str:
        return self.image.url

class Inventory(TimeStampedModel):
    UNITS = (
        ('piece', 'Piece'),
        ('meter', 'Meter')
    )
    
    uniform = models.OneToOneField(Uniform, on_delete=models.CASCADE, related_name='inventory', primary_key=True)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=15, choices=UNITS, default='piece')
    
    
    @property
    def quantity_text(self):
        return f'{self.quantity} {self.unit}(s)'
        
    def __str__(self) -> str:
        return self.uniform.name

    class Meta:
        verbose_name_plural = 'inventories'