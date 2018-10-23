from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from ScrummerTimes.choices import CATEGORIES

from comments.models import Comment


class Article(models.Model):
    title = models.CharField(max_length=200,  blank=True)
    header_image = models.ImageField(upload_to='header_image', blank=True, null=True)
    text = models.TextField(blank=True)
    is_read = models.BooleanField(blank=False, default=False)
    #The user who made the Article, read up on on_delete ups :)
    authors = models.ForeignKey(User, on_delete=models.PROTECT, null = True)
    category = models.CharField(max_length=20, choices=CATEGORIES)

    @property
    def comments(self):
        instance = self
        comments = Comment.filter_by_instance(instance)
        return comments

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

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