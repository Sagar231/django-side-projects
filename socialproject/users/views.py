from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import LoginForm,UserRegistrationForm, UserEditForm,ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post
# Create your views here.

def userlogin(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user= authenticate(
                    request,username = data['username'],
                    password=data['password']
                    )
            if user:
                login(request,user)
                return HttpResponse('user authenticated and logged in')
            else:
                return HttpResponse('invalid credentials')
    else:
        form = LoginForm()
    # return HttpResponse('cant show form')
    return render(request,'users/login.html',{'form':form})


def user_logout(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required
def index(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user)
    profile = Profile.objects.filter(user=current_user).first()
    return render(request,'users/index.html',{"posts":posts,'profile':profile})


def register(request):
    if request.method =='POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'users/register_done.html')
    else:
        user_form = UserRegistrationForm()

    return render(request,'users/register.html',{'user_form':user_form})

@login_required
def edit(request):
    if request.method=="POST":
        user_form = UserEditForm(
                                 instance=request.user,
                                 data=request.POST
                                 )
        profile_form = ProfileEditForm(
                                       instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES
                                       )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(
                                 instance=request.user,
                                 )
        profile_form = ProfileEditForm(
                                       instance=request.user.profile,
                                       )
    return render(request,'users/edit.html',{'user_form':user_form,"profile_form":profile_form})
        


