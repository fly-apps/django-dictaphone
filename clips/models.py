from django.db import models

class Clip(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True)
    mime = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name