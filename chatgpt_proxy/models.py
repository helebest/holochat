from django.db import models


# Create your models here.

class Message(models.Model):
    timestamp = models.DateTimeField('timestamp')
    role = models.CharField(max_length=16)
    content = models.CharField(max_length=4096)
