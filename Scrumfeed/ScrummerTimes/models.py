from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


from comments.models import Comment


class Article(models.Model):
    title = models.CharField(max_length=200,  blank=True)
    header_image = models.ImageField(upload_to='header_image', default='header_image/NoImage.jpg', blank=True,
                                     null=True)
    first_text = models.TextField(blank=True)
    in_line_image = models.ImageField(upload_to='in_line_image', blank=True, null=True)
    second_text = models.TextField(blank=True)
    is_read = models.BooleanField(blank=False, default=False)
    # on_delete = models.CASCADE means that if the author is deleted, then the articles are also deleted
    authors = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    # on_delte=models.SET_NULL means if the category is deleted, the catagory is set to null
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    draft = models.BooleanField(blank=False, default=False)
    editors = models.ForeignKey(User, null=True, blank=True, related_name='editor', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(blank=False, default=False)

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


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        # Make it say "categories" instead of the default "categorys"
        verbose_name_plural = "categories"
        permissions = (
            ("edit_categories", "can delete and add categories"),
        )

    def __str__(self):
        return self.name.__str__()


class role(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        # Make it say "categories" instead of the default "categorys"
        verbose_name_plural = "categories"
        permissions = (
            ("edit_categories", "can delete and add categories"),
        )

    def __str__(self):
        return self.name.__str__()