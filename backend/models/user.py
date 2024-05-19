from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from . extras import TimeStampedModel

__all__ = ['User', 'Department']

class Department(TimeStampedModel):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)    
    
    def __str__(self) -> str:
        return f"{self.name}"

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('student', 'Student')
    )

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    department = models.ForeignKey(Department, null=True, blank=True, related_name='members', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, choices=ROLES, default='student')
    middle_name = models.CharField(max_length=150,  null=True, blank=True)
    suffix = models.CharField(max_length=150,  null=True, blank=True)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)
    mobile_number = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, null=True)
    student_id = models.CharField(max_length=150, null=True, unique=True)
    photo = models.ImageField(upload_to='user/photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    @property
    def get_full_name(self):
        return f'{self.first_name or ""} {self.middle_name or ""} {self.last_name or ""} {self.suffix or ""}'
    
    @property
    def get_short_name(self):
        first_name_0 = f'{self.first_name[0]}.' if self.first_name else '.'
        return f'{first_name_0} {self.last_name}'
    
    @property
    def get_status(self):
        return 'active' if self.is_active else 'inactive'
    
    @property
    def default_photo_url(self):        
        return f"{settings.STATIC_URL}frontend/img/default-profile.webp"
    
    @classmethod
    def count(cls):
        query = cls.objects.all()        
        return query.aggregate(count=models.Count('id'))['count']
        
        
        
       
    