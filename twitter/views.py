from django.shortcuts import render
from . models import tweet
from . forms import Tweetform,UserRegistration
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def index(request):
    return render(request,'index.html')

def tweet_list(request):
    tweets = tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html', {'tweets' : tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = Tweetform(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = Tweetform()
    return render(request,'tweet_form.html', {'form' : form})

@login_required
def tweet_edit(request, tweet_id):
    tweet_instance = get_object_or_404(tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = Tweetform(request.POST, request.FILES, instance=tweet_instance)
        if form.is_valid():
            form.save()  # No need to reassign tweet.user, as it's already associated with the instance
            return redirect('tweet_list')  # Redirect to the tweet list or another appropriate view
    else:
        form = Tweetform(instance=tweet_instance)
    
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet_instance = get_object_or_404(tweet, pk = tweet_id, user = request.user)
    if  request.method == "POST":
        tweet_instance.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet' : tweet})

def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistration()
    
    return render(request, 'registration/register.html', {'form' : form})