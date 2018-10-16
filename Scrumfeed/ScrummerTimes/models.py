from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200,  blank=True)
    header_image = models.ImageField(upload_to='header_image',default='header_image/NoImage.jpg', blank=True, null=True)
    text = models.TextField(blank=True)
    is_read = models.BooleanField(blank=False, default=False)
    #on_delete = models.CASCADE means that if the author is deleted, then the articles are also deleted
    authors = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    #category = models.CharField(max_length=20, choices=CATEGORIES)
    #on_delte=models.SET_NULL means if the category is deleted, the catagory is set to null
    category = models.ForeignKey('Category', null=True, blank=True, on_delete= models.SET_NULL)
    # tetsetsettestestestsetststest
    def __str__(self):
        return self.title.__str__()


    #Custom permisions for this object Article.
    #Review and publish are permissions for Editors
    #Create_article are for Authors
    #To use these, write something like @permission_required('ScrummerTimes.review_article', login_url='/accounts/login/')
    class Meta:
        permissions = (
            ("create_article", "can create an article on the site"),
            ("review_article", "can review an article, for editors"),
            ("publish_article", "can publish an article")
        )

class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        #Make it say "categories" instead of the default "categorys"
        verbose_name_plural = "categories"
        permissions = (
            ("edit_categories", "can delete and add categories"),
        )

    def __str__(self):
        return self.name.__str__()
