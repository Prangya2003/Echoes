from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model,authenticate,login,logout
from .models import UserProfileModel,UserRelationModel
from posts.models import PostModel,SavedPostModel
from message.models import RecipientModel

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        post_data = PostModel.objects.exclude(user__pk=request.user.pk)
        return render(request, 'home.html',context={"user":request.user,"posts":post_data})
    else:
        return redirect('login_view')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_instance = authenticate(username=username, password=password)
        if user_instance is not None:
            login(request,user_instance)
            return redirect('home_view')
        else:
            print("Invalid username or password")
            return redirect('login_view')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user_instance = get_user_model().objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        user_instance.set_password(password)
        user_instance.save()
        UserProfileModel.objects.create(user=user_instance) 
        UserRelationModel.objects.create(user=user_instance) 
        RecipientModel.objects.create(user=user_instance) 
        SavedPostModel.objects.create(user=user_instance)
        return redirect('login_view')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')

def profile_view(request, username):
    user_instance = get_object_or_404(get_user_model(), username=username)
    count = {
        "posts_count": user_instance.PostModel_user.all().count(),
        "followers_count": user_instance.UserRelationModel_user.followers.all().count(),
        "following_count": user_instance.UserRelationModel_user.following.all().count()
    }
    return render(request, 'profile.html', context={"user": user_instance, "count": count})