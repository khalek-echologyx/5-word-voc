from django.db import models

class User(models.Model):
    device_id = models.CharField(max_length=225, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.device_id