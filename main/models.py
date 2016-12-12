from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
    Model to auto add updated/created fields to models
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


