from django.db import models
from django.conf import settings

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=300)



class Event(models.Model):
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events")
    image = models.ImageField(null=True, blank=True, default='no_image.jpg')
    name  = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    