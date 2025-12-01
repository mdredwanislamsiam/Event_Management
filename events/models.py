from django.db import models



class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=300)

class Participant(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()



class Event(models.Model):
    participant = models.ManyToManyField(Participant, related_name="events")
    image = models.ImageField(null = True, blank= True)
    name  = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    