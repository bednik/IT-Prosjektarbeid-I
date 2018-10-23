from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from ScrummerTimes.choices import CATEGORIES

from comments.models import Comment


class Article(models.Model):
    title = models.CharField(max_length=200,  blank=True)
    header_image = models.ImageField(upload_to='header_image', blank=True, null=True)
    first_text = models.TextField(blank=True)
    in_line_image = models.ImageField(upload_to='in_line_image', blank=True, null=True)
    second_text = models.TextField(blank=True)
    is_read = models.BooleanField(blank=False, default=False)
    #The user who made the Article, read up on on_delete ups :)
    authors = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    draft = models.BooleanField(blank=False, default=False)
    editors = models.ForeignKey(User, null=True, blank=True, related_name='editor', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

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

    # Custom permisions for this object Article.
    # Review and publish are permissions for Editors
    # Create_article are for Authors
    # To use these, write something like @permission_required('ScrummerTimes.review_article',
    # login_url='/accounts/login/')
    class Meta:
        permissions = (
            ("create_article", "can create an article on the site"),
            ("review_article", "can review an article, for editors"),
            ("publish_article", "can publish an article"),
            ("save_as_draft", "can save article as draft"),
        )
