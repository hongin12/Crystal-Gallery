from django.db import models
from django.db import models


class User_Profile(models.Model):
    name = models.CharField(max_length=200, default=None)
    price = models.IntegerField(default=None)
    #explanation = models.CharField(max_length=500)
    email = models.EmailField(default = None)
    display_picture = models.FileField(default=None)

    def __str__(self):
        return self.fname
# Create your models here.
