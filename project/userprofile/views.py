from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model,authenticate,login,logout
from .models import UserProfileModel,UserRelationModel
from posts.models import PostModel,SavedPostModel
from message.models import RecipientModel

# Create your views here.
def home_view(request):
    if request.method == 'POST':
        if get_user_model().objects.filter(username=request.POST.get('username')).exists():
            return redirect('profile_view', request.POST.get('username'))
    if request.user.is_authenticated:
        post_data = PostModel.objects.exclude(user__pk=request.user.pk).order_by('-created_at')
        return render(request, 'home.html',context={"request":request,"user":request.user,"posts":post_data})
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
    error_flag = False
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if get_user_model().objects.filter(username=username).exists():
            messages.error(request,"Username is already taken")
            error_flag = True
        else:
            user_instance = get_user_model().objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
            user_instance.set_password(password)
            user_instance.save()
            UserProfileModel.objects.create(user=user_instance) 
            UserRelationModel.objects.create(user=user_instance) 
            RecipientModel.objects.create(user=user_instance) 
            SavedPostModel.objects.create(user=user_instance)
        if not error_flag:
            return redirect('login_view')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')

def profile_view(request,username):
    user_instance = get_user_model().objects.get(username=username)
    data = {
        "is_user_profile": True if request.user.username == username else False,
        "posts_count":user_instance.PostModel_user.all().count(),
        "saved_posts_count":user_instance.SavedPostModel_user.posts.all().count(),
        "followers_count":user_instance.UserRelationModel_user.followers.all().count(),
        "following_count":user_instance.UserRelationModel_user.following.all().count(),
        "user_posts":user_instance.PostModel_user.all(),
        "user_saved_posts":user_instance.SavedPostModel_user.posts.all()
    }
    print(data['is_user_profile'])
    return render(request, 'profile.html',context={"request":request,"user":user_instance,"data":data})

def update_user_profile(request):
    user_instance= request.user
    if request.method == 'POST':
        user_instance.first_name = request.POST.get('first_name')
        user_instance.last_name = request.POST.get('last_name')
        if request.POST.get('username') != request.user.username:
            if get_user_model().objects.filter(username=request.POST.get('username')).exists():
                print("Username already taken")
            else:
                user_instance.username = request.POST.get('username')
        user_profile_instance = user_instance.UserProfileModel_user
        user_profile_instance.bio = request.POST.get('bio')
        if len(request.FILES) != 0:
            user_profile_instance.profile_picture = request.FILES['profile_picture']
        user_profile_instance.save()
        user_instance.save()
        return redirect('profile_view',username=request.user.username)
    return render(request, 'update_user_profile.html',context={"request":request,"user":request.user})

def update_password_view(request):
    user_instance = request.user
    if request.method == 'POST':
        user_check = authenticate(username=user_instance.username,password=request.POST.get('password'))
        if user_check is not None:
            if request.POST.get('new_password') == request.POST.get('new_password_check'):
                user_instance.set_password(request.POST.get('new_password'))
                user_instance.save()
        return redirect('profile_view',request.user.username)
    return render(request, 'update_password.html',context={"request":request,"user":request.user})

def delete_profile_view(request):
    request.user.delete()
    return redirect('login_view')

def follow_view(request,username):
    user_instance = request.user
    user_relation_instance = request.user.UserRelationModel_user

    target_user = get_user_model().objects.get(username=username)
    target_user_relation_instance = target_user.UserRelationModel_user

    if user_relation_instance.following.all().filter(id=target_user.id).exists():
        user_relation_instance.following.remove(target_user)
    else:
        user_relation_instance.following.add(target_user)
    user_relation_instance.save()

    if target_user_relation_instance.followers.all().filter(id=user_instance.id).exists():
        target_user_relation_instance.followers.remove(user_instance)
    else:
        target_user_relation_instance.followers.add(user_instance)
    target_user_relation_instance.save()
    return redirect('profile_view',username=username)


def like_view(request,id):
    post_instance = PostModel.objects.get(id=id)
    if post_instance.likes.all().filter(username=request.user.username).exists():
        post_instance.likes.remove(request.user)
    else:
        post_instance.likes.add(request.user)
    post_instance.save()
    return redirect('home_view')

def save_view(request,id):
    post_instance = PostModel.objects.get(id=id)
    saved_post_instance = request.user.SavedPostModel_user
    if saved_post_instance.posts.all().filter(id=id).exists():
        saved_post_instance.posts.remove(post_instance)
    else:
        saved_post_instance.posts.add(post_instance)
    saved_post_instance.save()
    return redirect('home_view')

def followers_view(request,username):
    user_instance = get_user_model().objects.get(username=username)
    data = {
        "user":user_instance,
        "followers":user_instance.UserRelationModel_user.followers.all()
    }
    return render(request, 'followers.html',context={"request":request,"data":data})

def following_view(request,username):
    user_instance = get_user_model().objects.get(username=username)
    data = {
        "user":user_instance,
        "followings":user_instance.UserRelationModel_user.following.all()
    }
    return render(request, 'following.html',context={"request":request,"data":data})