from datetime import datetime


from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200,  blank=True)
    header_image = models.ImageField(upload_to='header_image', blank=True, null=True)
    text = models.TextField(blank=True)
    is_read = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.title.__str__()


    #Custom permisions for this object Article.
    #Review and publish are permissions for Editors
    #Any user can create an article
    #To use these, write something like @permission_required('ScrummerTimes.review_article', login_url='/accounts/login/')
    class Meta:
        permissions = (
            ("create_article", "can create an article on the site"),
            ("review_article", "can review an article, for editors"),
            ("publish_article", "can publish an article")
        )