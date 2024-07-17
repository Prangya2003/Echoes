from django.contrib import admin
from .models import MessageModel,RecipientModel

# Register your models here.
admin.site.register(MessageModel)
admin.site.register(RecipientModel)