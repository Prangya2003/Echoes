from django.contrib import admin
from .models import UserProfileModel,UserRelationModel

# Register your models here.
admin.site.register(UserProfileModel)
admin.site.register(UserRelationModel)