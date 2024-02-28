from django.shortcuts import render
from .forms import LoginForm

# Create your views here.

def userlogin(request):
    form = LoginForm()
    return render(request,'users/login.html',{'form':form})