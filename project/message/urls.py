from django.urls import path
from .views import message_view,recipient_message_view

urlpatterns = [
    path('message/',message_view,name="message_view"),
    path('message/<str:username>/', recipient_message_view, name="recipient_message_view"),
]