from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user

from . import models

def must_be_unique(value):
    user_objects = auth_user.objects.filter(email=value)
    if len(user_objects) > 0:
        raise forms.ValidationError("Email already exists")
    # Always return the cleaned data
    return value

class UpdateAboutForm(forms.Form):
    about = forms.CharField(
        label="About",
        required=False
    )

    def save(self, request, name):
        user_instance = models.UserModel.objects.get(username=name)
        user_instance.about = self.cleaned_data["about"]
        user_instance.save()
        return user_instance

class UpdatePictureForm(forms.Form):
    profile_picture = forms.ImageField(
        label="Profile Picture",
        required=True
    )

    def save(self, request, name):
        user_instance = models.UserModel.objects.get(username=name)
        user_instance.profile_picture = self.cleaned_data["profile_picture"]
        user_instance.save()
        return user_instance

class CommunityForm(forms.Form):
    community_field = forms.CharField(
        label='Community',
        max_length=120,
        )
    about_field = forms.CharField(
        label='About',
        max_length=500,
    )

    def save(self, request):
        community_instance = models.CommunityModel()
        community_instance.community = self.cleaned_data["community_field"]
        community_instance.about = self.cleaned_data["about_field"]
        community_instance.save()
        return community_instance

    def getCommunityName(self, request):
        return self.cleaned_data["community_field"]



class SuggestionForm(forms.Form):
    suggestion_field = forms.CharField(
        label='Suggestion',
        max_length=240,
        #validators=[must_be_unique]
        )
    image = forms.ImageField(
        label="Image File",
        required=False
    )
    image_description = forms.CharField(
        label="Image Description",
        max_length=240,
        required=False
    )

    def save(self, request, community_id):
        community_instance = models.CommunityModel.objects.get(community=community_id)
        suggestion_instance = models.SuggestionModel()
        suggestion_instance.suggestion = self.cleaned_data["suggestion_field"]
        suggestion_instance.image = self.cleaned_data["image"]
        suggestion_instance.image_description = self.cleaned_data["image_description"]
        suggestion_instance.author = request.user
        suggestion_instance.community = community_instance
        suggestion_instance.save()
        return suggestion_instance

class CommentForm(forms.Form):
    comment_field = forms.CharField(
        label='Comment',
        max_length=240,
        # validators=[validate_unicode_slug, must_be_caps, must_be_bob]
        )

    def save(self, request, community_id, sugg_id):
        community_instance = models.CommunityModel.objects.get(community=community_id)
        suggestion_instance = models.SuggestionModel.objects.get(id=sugg_id)
        comment_instance = models.CommentModel()
        comment_instance.comment = self.cleaned_data["comment_field"]
        comment_instance.author = request.user
        comment_instance.suggestion = suggestion_instance
        comment_instance.community = community_instance
        comment_instance.save()
        return comment_instance

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = auth_user
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def saveUser(self, commit=True):
        user_instance = models.UserModel()
        user_instance.username = self.cleaned_data["username"]
        user_instance.first_name = self.cleaned_data["first_name"]
        user_instance.last_name = self.cleaned_data["last_name"]
        if commit:
            user_instance.save()
        return user_instance

