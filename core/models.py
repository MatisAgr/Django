from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200) #équivalent de varchar en SQL
    completed = models.BooleanField(default=False) #case à cocher
    created_at = models.DateTimeField(auto_now_add=True) #mettre date/heure auto
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
