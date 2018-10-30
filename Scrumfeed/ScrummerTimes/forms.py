import hashlib
import io

from PIL import Image
from django.core.exceptions import ValidationError
from django.forms import forms, CharField, IntegerField, ImageField, ChoiceField
from django.core.files.base import ContentFile
from django.forms import forms, CharField, IntegerField, ImageField, URLField, TypedChoiceField, RadioSelect, BooleanField, Textarea, ModelChoiceField
from .models import Article, Category, Role
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.models import Permission

from django.forms import *


# Noe tull
class ArticleForm(forms.Form):
    title = CharField(max_length=120)
    # Required has to be False, cant publish article if it is false
    header_image = ImageField(required=False)
    draft = BooleanField(required=False, initial=False)
    first_text = CharField(widget=Textarea)
    in_line_image = ImageField(required=False)
    second_text = CharField(widget=Textarea)
    # category = ChoiceField(choices=CATEGORIES, required=False)
    is_read = BooleanField(required=False, initial=False)
    # category = ChoiceField(choices=CATEGORIES, required=False)
    category = ModelChoiceField(queryset=Category.objects.all())

    theme = ChoiceField(choices=Article.THEMES, initial=1)
    is_completed = BooleanField(required=False, initial=False)

    class Meta:
        # The two below has something to do with assigning who the author of the article is
        model = Article
        exclude = ('user',)

    # Check if the things that is written in the form are valid
    def clean(self):
        return self.cleaned_data


class RequestRole(forms.Form):
    reason = CharField(widget=Textarea, required=False)

    role = ChoiceField(choices=Role.ROLE_TYPES, required=True)

    def clean(self):
        return self.cleaned_data


class FilterForm(forms.Form):
    # category = ChoiceField(choices=CATEGORIES)
    category = ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Article

    # Check if the things that is written in the form are valid
    def clean(self):
        return self.cleaned_data


class CreateCategoryForm(forms.Form):
    category = ModelChoiceField(queryset=Category.objects.all(), required = False)
    name = CharField(max_length=50, required= False)

    class Meta:
        model = Category

    def clean(self):
        name = self.cleaned_data['name']
        # if(name == '' or name == None):
        #    raise ValidationError({'name': "Your category can not be blank"}, code='invalid')
        if ' ' in name:
            # raise ValidationError({'name': "Your category can not have spaces"}, code='invalid')
            raise forms.ValidationError("Your category can not have spaces", code='invalid')
        if Category.objects.filter(name = name).exists():
            raise forms.ValidationError("A category with this name already exists", code='invalid')
        return self.cleaned_data


class DeleteForm(forms.Form):

    class Meta:
        model = Article

    def clean(self):
        return self.cleaned_data


class NewCommentForm(forms.Form):
    content_type = CharField(widget=HiddenInput)
    object_id = IntegerField(widget=HiddenInput)
    parent_id = IntegerField(widget=HiddenInput, required=False)
    content = CharField(widget=Textarea, required=False)


# Drop-down bar for editors




class FilterEditor(forms.Form):
    copyeditor = ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super(FilterEditor, self).__init__(*args, **kwargs)
        perm = Permission.objects.get(codename='review_article')
        perm2 = Permission.objects.get(codename='publish_article')
        self.fields['copyeditor'].queryset = User.objects.filter(Q(user_permissions=perm)).filter(~Q(user_permissions=perm2)).distinct()
    # Check if the things that is written in the form are valid
    def clean(self):
        return self.cleaned_data
