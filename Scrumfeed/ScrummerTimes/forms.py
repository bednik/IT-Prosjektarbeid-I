from django.core.exceptions import ValidationError
from django.forms import forms, CharField, IntegerField, ImageField, ChoiceField
from ScrummerTimes.choices import CATEGORIES

# Noe tull
class ArticleForm(forms.Form):
    title = CharField(max_length=120)
    header_image = ImageField()
    text = CharField()
    category = ChoiceField(choices=CATEGORIES,)

    #Check if the things that is written in the form are valid
    def clean(self):
        return self.cleaned_data

        #try:
        #    if self.cleaned_data["description"].startswith(" "):
        #        raise ValidationError({'name': "Input cannot start with a space"}, code='invalid')
        #except KeyError:
        #    raise ValidationError({'name': "Description must be provided"}, code='invalid')
        #return self.cleaned_data
