from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length = 150, unique = True)
    username = models.CharField(max_length = 80, blank=True, null=True)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username","password"]
    
    def __str__(self):
        return f"{self.email}:{self.username}"