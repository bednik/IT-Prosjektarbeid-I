import hashlib
import io

from PIL import Image
from django.core.exceptions import ValidationError
from django.forms import forms, CharField, IntegerField, ImageField, ChoiceField
from ScrummerTimes.choices import CATEGORIES
from django.core.files.base import ContentFile
from django.forms import forms, CharField, IntegerField, ImageField, URLField, TypedChoiceField, RadioSelect, BooleanField, Textarea
from ScrummerTimes.models import Article

# Noe tull
class ArticleForm(forms.Form):
    title = CharField(max_length=120)
    # Required has to be False, because i did not find a way that i could edit an article without uplouding an image again.
    header_image = ImageField(required=False)
    first_text = CharField(widget=Textarea)
    in_line_image = ImageField(required=False)
    second_text = CharField(widget=Textarea)
    category = ChoiceField(choices=CATEGORIES, required=False)
    is_read = BooleanField(required=False, initial=False)

    class Meta:
        # The two below has something to do with assigning who the author of the article is
        model = Article
        exclude = ('user',)

    #Check if the things that is written in the form are valid
    def clean(self):
        return self.cleaned_data

        #try:
        #    if self.cleaned_data["description"].startswith(" "):
        #        raise ValidationError({'name': "Input cannot start with a space"}, code='invalid')
        #except KeyError:
        #    raise ValidationError({'name': "Description must be provided"}, code='invalid')
        #return self.cleaned_data


class FilterForm(forms.Form):
    category = ChoiceField(choices=CATEGORIES)

    class Meta:
        model = Article

    #Check if the things that is written in the form are valid
    def clean(self):
        return self.cleaned_data

        #try:
        #    if self.cleaned_data["description"].startswith(" "):
        #        raise ValidationError({'name': "Input cannot start with a space"}, code='invalid')
        #except KeyError:
        #    raise ValidationError({'name': "Description must be provided"}, code='invalid')
        #return self.cleaned_data

