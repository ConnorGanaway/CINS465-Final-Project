from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.UserModel)
admin.site.register(models.CommunityModel)
admin.site.register(models.SuggestionModel)
admin.site.register(models.CommentModel)
