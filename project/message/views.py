from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .models import MessageModel
from django.db.models import Q

# Create your views here.
def message_view(request):
    data = {
        "recipients": request.user.RecipientModel_user.recipients.all()
    }
    return render(request, 'message.html', context={"request": request, "data": data})

def recipient_message_view(request,username):
    recipient_user = get_user_model().objects.get(username=username)
    recipient_instance = recipient_user.RecipientModel_user

    user_instance = request.user
    user_recipient_instance = user_instance.RecipientModel_user

    if not recipient_instance.recipients.all().filter(username=user_instance.username).exists():
        recipient_instance.recipients.add(request.user)
        recipient_instance.save()

    if not user_recipient_instance.recipients.all().filter(username=recipient_user.username).exists():
        user_recipient_instance.recipients.add(recipient_user)
        user_recipient_instance.save()

    if request.method == "POST":
        MessageModel.objects.create(sender=user_instance,recipient=recipient_user,message=request.POST.get('message'))
        return redirect('recipient_message_view',username)

    data = {
        "recipients": user_recipient_instance.recipients.all(),
        "sender": user_instance.username,
        "receiver": recipient_user.username,
        "messages" : MessageModel.objects.filter(Q(sender=user_instance, recipient=recipient_user) |Q(sender=recipient_user, recipient=user_instance)).order_by('created_at')

    }
    

    return render(request,"message.html",context={"request":request, "data":data})