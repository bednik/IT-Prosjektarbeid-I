from datetime import datetime

from django.db import models
from ScrummerTimes.choices import CATEGORIES

class Article(models.Model):
    title = models.CharField(max_length=200,  blank=True)
    header_image = models.ImageField(upload_to='header_image', blank=True)
    text = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)

    def __str__(self):
        return self.title.__str__()