from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    is_intern = models.BooleanField(default=False)
    user_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_mentor:
            self.status = False  # Admin approval needed
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    
    