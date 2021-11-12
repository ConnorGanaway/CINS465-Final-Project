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
        return

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
