from django.db import models

# Create your models here.
class Bookmark (models.Model):
    id = models.IntegerField()
    title = models.CharField(max=255)
    url = models.URLField()
    notes = models.TextField()
    date_added = models.DateField()