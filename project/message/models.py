from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class MessageModel(models.Model):
    sender = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="MessageModel_sender",null=True)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="MessageModel_recipient",null=True)
    message = models.TextField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)

class RecipientModel(models.Model):
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name="RecipientModel_user",null=True)
    recipients = models.ManyToManyField(get_user_model(), related_name="RecipientModel_recipients",blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)