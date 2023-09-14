from django.db import models
from .validators import validate_file_extension
from django.db.models import JSONField


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='documents/',validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)


#haystack schema definition

class DocumentDataStore(models.Model):
    title = models.CharField(max_length=200)
    extracted_text = models.TextField()

    def __unicode__(self):
        return self.title


# Dashboard Charts info

class ChartInfo(models.Model):
    numbers_of_file_uploaded = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class ChartsNLP(models.Model):
    nlp_data = models.JSONField(default=dict)

class ChartFolderQuotas(models.Model):
    folder_size = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


