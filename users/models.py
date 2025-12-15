from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser): 
    phone_number = models.CharField(max_length=15, blank= True)
    profile_image = models.ImageField(upload_to='profile_images', blank = True)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    def __str__(self): 
        return self.username