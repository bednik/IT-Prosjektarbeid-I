from datetime import datetime

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200,  blank=True)
    header_image = models.ImageField(upload_to='header_image', blank=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.title.__str__()


