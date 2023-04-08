from django.db import models


# Create your models here.
class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
