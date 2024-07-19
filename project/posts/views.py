from django.shortcuts import render,redirect,get_object_or_404
from .models import PostModel,CommentModel

# Create your views here.
def create_post_view(request):
    if request.method == 'POST':
        PostModel.objects.create(
            user=request.user,
            post=request.FILES['post'],
            caption=request.POST.get('caption')
        )
        username = request.user.username
        return redirect('profile_view', username=username)
    return render(request, 'create_post.html')

def view_post(request,id):
    post_instance = PostModel.objects.get(id=id)
    if request.method == 'POST':
        comment_instance = CommentModel.objects.create(user=request.user, comment=request.POST.get('comment'))
        post_instance.comments.add(comment_instance)
        post_instance.save()
        redirect('view_post',id)
    return render(request, 'view_post.html', context={"request":request,"user":request.user,"post":post_instance})

def post_like_view(request,id):
    post_instance = PostModel.objects.get(id=id)
    if post_instance.likes.all().filter(username=request.user.username).exists():
        post_instance.likes.remove(request.user)
    else:
        post_instance.likes.add(request.user)
    post_instance.save()
    return redirect('view_post',id)

def post_save_view(request,id):
    post_instance = PostModel.objects.get(id=id)
    saved_post_instance = request.user.SavedPostModel_user
    if saved_post_instance.posts.all().filter(id=id).exists():
        saved_post_instance.posts.remove(post_instance)
    else:
        saved_post_instance.posts.add(post_instance)
    saved_post_instance.save()
    return redirect('view_post',id)

def update_post_view(request,id):
    post_instance = PostModel.objects.get(id=id)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            post_instance.post = request.FILES['post']
        post_instance.caption = request.POST.get('caption')
        post_instance.save()
        return redirect('view_post',id)
    return render(request, 'update_post.html', context={"request":request,"user":request.user,"post":post_instance})

def delete_post_view(request, id):
    post_instance = get_object_or_404(PostModel, id=id)

    if post_instance.user == request.user:
        post_instance.delete()
        username = request.user.username
        return redirect('profile_view', username=username)
    else:
        # Handle unauthorized deletion attempt
        return render(request, 'error.html', {'message': 'You are not authorized to delete this post.'})