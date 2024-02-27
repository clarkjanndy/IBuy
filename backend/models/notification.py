from django.db import models
from . extras import TimeStampedModel

from . user import User

__all__ = ['Notification',]

class Notification(TimeStampedModel):    
    STATUS = (
        ('unseen', 'Unseen'),
        ('seen', 'Seen')
    )
    
    LEVEL = (
        ('primary', 'Primary'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('danger', 'Danger')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    level = models.CharField(max_length=8, default='others', choices=LEVEL)
    content = models.TextField()
    link = models.CharField(max_length = 100)
    status = models.CharField(max_length=8, default='unseen', choices=STATUS)
    
    def __str__(self):
        return f"{self.user}"
    
    