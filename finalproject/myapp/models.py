from django.db import models
from django.contrib.auth.models import User as auth_user

# Create your models here.

class UserModel(models.Model):
    username = models.CharField(max_length=240)
    profile_picture = models.ImageField(
        max_length = 144,
        upload_to = 'uploads/profiles/',
        null=True
    )
    followed_communities = models.TextField(null=True)
    numPosts = models.IntegerField(default=0)

    def __str__(self):
        return str(self.username)


class CommunityModel(models.Model):
    community = models.CharField(max_length=120)
    about = models.CharField(
        default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        max_length=500
    )

    def __str__(self):
        return str(self.community)


class SuggestionModel(models.Model):
    suggestion = models.CharField(max_length=240)
    author = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    community = models.ForeignKey(CommunityModel, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField(default=0)
    image = models.ImageField(
        max_length = 144,
        upload_to = 'uploads/%Y/%m/%d/',
        null=True
    )
    image_description = models.CharField(
        max_length=240,
        null=True
    )

    def __str__(self):
        return str(self.author.username) + " " + str(self.suggestion)

class CommentModel(models.Model):
    comment = models.CharField(max_length=240)
    author = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    community = models.ForeignKey(CommunityModel, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(SuggestionModel, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author.username) + " " + str(self.comment)
