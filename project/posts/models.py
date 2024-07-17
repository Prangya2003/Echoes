from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class CommentModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="CommentModel_user",null=True)
    comment = models.CharField(max_length=100,null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)

class PostModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="PostModel_user",null=True)
    post = models.ImageField(upload_to="posts/", blank=True, null=True)
    caption = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name="PostModel_likes", blank=True)

    comments = models.ManyToManyField(CommentModel, related_name="PostModel_comments", blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

class SavedPostModel(models.Model):
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name="SavedPostModel_user",null=True)
    posts = models.ManyToManyField(PostModel,related_name="SavedPostModel_posts",blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    