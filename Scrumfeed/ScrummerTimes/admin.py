from django.contrib import admin
from accounts.models import UserProfile
# Register your models here.
from .models import Article, Category

##Sup dudesafsa
admin.site.register(Article)

admin.site.register(Category)

admin.site.register(UserProfile)
