from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.models import User, auth
from account.forms import RegistrationForm,VideoForm, EditProfileForm
from account.models import Account
from .models import Video,Comment,Like
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


def registration_view(request):
    context={}
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            phone=form.cleaned_data.get('phone')
            password=form.cleaned_data.get('password1')
            account=authenticate(phone=phone,password=password)
            login(request,account)
            logout(request)
            return redirect('login')
        else:
            context['registration_form']=form
    else:
        form=RegistrationForm()
        context['registration_form']=form
    return render(request,'register.html',context)
# Create your views here.

def home(request):
    return render(request,'homepage.html')

def login1(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        user = auth.authenticate(phone=phone, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request,'Invalid Phone or Password')
            return redirect('login')

    if request.user.is_authenticated:
        return redirect('home')


    return render(request,'login.html')




'''def User1(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        points = request.POST.get('points')
        streams = request.POST.get('streams')
        upvotes = request.POST.get('upvotes')
        points_donated = request.POST.get('points_donated')
        user = User(phone=phone, points=points, streams=streams, upvotes=upvotes, points_donated=points_donated)
        user.save()

    user = User.objects.filter(phone=phone)
    return render(request, 'homepage.html', {'user': user})

    # return render(request, 'homepage.html')'''

def logout1(request):
    auth.logout(request)
    return redirect('login')


def vid(request): 
    vids = Video.objects.all().order_by("-time")
    return render(request, 'recently_added.html', {'vids' : vids})


def showimage(request):#, phone_id): 
    '''if request.method == 'POST': 
        form = ImageForm(request.POST, request.FILES)
  
        if form.is_valid(): 
            obj = form.save(commit = False) 
            obj.user = request.user
            obj.save()
            form=ImageForm() 
            
    else: 
        form = ImageForm() 
    return render(request, 'new.html', {'form' : form}) '''
    #obj_record = get_object_or_404(Account, pk=phone_id)
    if not request.user.is_authenticated:
        return redirect('login')
    form = VideoForm(request.POST or None, request.FILES or None) 
    if request.method =='POST': 
          
        if form.is_valid(): 
              
            obj = form.save(commit = False) 
            obj.phone_id = request.user.phone
            obj.save()
            return HttpResponseRedirect(reverse(post, args=[obj.videoid]))
            #form = VideoForm() 
            #messages.success(request, "Successfully created") 
          
  
    return render(request, 'stream.html', {'form':form})

def readmore(request,videoid):
    if request.POST:
        message=request.POST['message']
        #user1=request.POST['user']
        post=Video.objects.get(videoid=videoid)
        user1=Account.objects.get(username=request.POST['user'])
        query=Comment(comment=message,post=post,user=user1)
        query.save()
    post=Video.objects.get(videoid=videoid)
    comment=Comment.objects.filter(post=videoid)
    com_user=request.user
    likes_count=Like.objects.get(post=videoid).user.count()
    if not request.user.is_authenticated:
        return render (request, 'readmore.html',{'post':post, 'comment':comment,'likes_count':likes_count})
    else:
        is_liked = Like.objects.filter(post=videoid,user=request.user).exists()    
        return render (request, 'readmore.html',{'post':post, 'comment':comment,'is_liked':is_liked,'likes_count':likes_count})

@login_required
def profile(request):
    vids = Video.objects.filter(phone=request.user).order_by('-time')
    return render(request,'profile.html', {'vids' : vids})

def LikePost(request):
    post_id=request.GET.get("likeId","")
    post=Video.objects.get(pk=post_id)
    user=request.user
    like=Like.objects.filter(post=post,user=user)
    liked=False

    if like:
        Like.dislike(post,user)
    else:
        liked=True
        Like.liked(post,user)
    try:
        likes_count=Like.objects.get(post=post_id).user.count() 
    except likes_count.DoesNotExist:
        likes_count=0
    resp={'liked':liked, 'likes_count':likes_count}
    response=json.dumps(resp)
    return HttpResponse(response,content_type="application/json")

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES,instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('profile'))
        else:
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'change_password.html', args)

def post(request,videoid):
    if request.POST:
        message=request.POST['message']
        #user1=request.POST['user']
        post=Video.objects.get(pk=videoid)
        user1=Account.objects.get(username=request.POST['user'])
        query=Comment(comment=message,post=post,user=user1)
        query.save()
    post=Video.objects.get(pk=videoid)
    comment=Comment.objects.filter(post=videoid)
    com_user=request.user
    likes_count={}
    try:
        likes_count=Like.objects.get(post=videoid).user.count() 
    except ObjectDoesNotExist:
        likes_count=0
    
    try:
        user_list=Like.objects.get(post=videoid).user.all()
    except ObjectDoesNotExist:
        user_list=''
    
    if not request.user.is_authenticated:
        return render (request, 'post.html',{'post':post, 'comment':comment,'likes_count':likes_count,'user_list':user_list})
    else:
        is_liked = Like.objects.filter(post=videoid,user=request.user).exists()    
        return render (request, 'post.html',{'post':post, 'comment':comment,'is_liked':is_liked,'likes_count':likes_count,'user_list':user_list})

def socialLogin(request):
    return render(request, 'socialLogin.html')

def triple(request):
    return render(request, 'triple.html')

def trending(request):
    return render(request, 'trending.html')

def duet(request):
    return render(request, 'duet.html')

@login_required
def pricing(request):
    return render(request, 'pricing.html')

def celeb(request):
    return render(request, 'celeb.html')

def User_Profile(request, username):
    username = Account.objects.get(username=username)
    vids = Video.objects.filter(phone=username).order_by('-time')
    return render(request, 'user_profile.html', {'username': username, 'vids':vids})

