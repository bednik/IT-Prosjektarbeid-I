from django.contrib import admin

# Register your models here.
from .models import Article, Category

##Sup dudesafsa
admin.site.register(Article)

admin.site.register(Category)