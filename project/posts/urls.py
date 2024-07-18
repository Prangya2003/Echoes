from django.urls import path
from .views import create_post_view,view_post,post_like_view,post_save_view,update_post_view,delete_post_view
urlpatterns = [
    path('create-post/',create_post_view,name='create_post_view'),
    path('view-post/<int:id>/',view_post,name='view_post'),
    path('like-post/<int:id>/',post_like_view,name='post_like_view'),
    path('save-post/<int:id>/',post_save_view,name='post_save_view'),
    path('update-post/<int:id>/',update_post_view,name='update_post_view'),
    path('delete-post/<int:id>/',delete_post_view,name='delete_post_view'),
]