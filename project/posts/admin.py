from django.contrib import admin
from .models import CommentModel,PostModel,SavedPostModel

# Register your models here.
admin.site.register(CommentModel)
admin.site.register(PostModel)
admin.site.register(SavedPostModel)