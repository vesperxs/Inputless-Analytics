from django.db import models
from django.db.models.base import Model

# Create your models here.

class save_email(models.Model):
    collected_mail = models.EmailField(max_length = 254)
