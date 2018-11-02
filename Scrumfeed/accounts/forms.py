from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import forms, CharField, IntegerField, ImageField
from accounts.models import UserProfile
from PIL import Image

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class EditUserProfile(forms.Form):
    description = CharField(max_length=200)
    phone = IntegerField(required = False)
    image = ImageField(required = False)

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def clean(self):
        return self.cleaned_data