urls py:
from django.contrib import admin
from django.urls import path
from pdf import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.accept,name="accept"),
    path('<int:id>/',views.resume,name="resume"),
    path('list/',views.list,name="list"),
]
 
 
accept html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <title>Document</title>
</head>
<body>
    <div class="container">
      <div class="row m-5">
        <div class="col-md-12">
          <h1>CV Generator</h1>
          <hr>
        </div>
      </div>
      <div class="row m-5">
        <div class="col-md-12">
          <h4>Please fill out your details</h4>
          
        </div>
      </div>
        <div class="row m-5">
            <div class="col-md-7">
                <form method="POST">
                    {% csrf_token %}
                    <div class="form-group">
                      <label for="">Name</label>
                      <input placeholder="Eg John Doe" type="text" class="form-control" id="name" name="name">
                    </div>
            
                    <div class="form-group">
                        <label for="">Email</label>
                        <input placeholder="Eg demo@gmail.com" type="text" class="form-control" id="email" name="email">
                      </div>
            
                      <div class="form-group">
                        <label for="">Phone</label>
                        <input placeholder="Eg 9999999999" type="text" class="form-control" id="phone" name="phone">
                      </div>
            
                      <div class="form-group">
                        <label for="">About You</label>
                        <textarea placeholder="Write something about you" type="text" class="form-control" id="summary" name="summary"></textarea>
                      </div>
                    
                      <div class="form-group">
                        <label for="">Degree</label>
                        <input placeholder="B-Tech Information Technology" type="text" class="form-control" id="degree" name="degree">
                      </div>
            
                      <div class="form-group">
                        <label for="">School</label>
                        <input placeholder="MIT" type="text" class="form-control" id="school" name="school">
                      </div>
            
            
                      <div class="form-group">
                        <label for="">University</label>
                        <input placeholder="MIT" type="text" class="form-control" id="university" name="university">
                      </div>
            
                      <div class="form-group">
                        <label for="">Previous Work</label>
                        <textarea placeholder="Programmer @ XYZ" type="text" class="form-control" id="previous_work" name="previous_work"></textarea>
                      </div>
            
                      <div class="form-group">
                        <label for="">Skills</label>
                        <textarea placeholder="eg C, C++, Python" type="text" class="form-control" id="skills" name="skills"></textarea>
                      </div>
                    
                    <button type="submit" class="btn btn-primary">Submit</button>
                  </form>
            </div>
        </div>
    </div>
</body>
</html>
 
list html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
 
    <title>Document</title>
</head>
<body>
    <div class="container">
        <div class="row m-5">
            <div class="col-md-12">
                <h2>CV Database Profile List</h2>
            </div>
 
        </div>
 
        {% for profile in profiles %}
        <div class="row">
            <div class="col-md-6">
                {‌{profile.name}}
            </div>    
            <div class="col-md-6">
                   <a href="/{‌{profile.id}}" class="btn btn-warning">Download CV</a>
                </div>  
        </div>
    <hr>
        {% endfor %}
    </div>
</body>
</html>
 
resume html
 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h2>{‌{user_profile.name}}</h2>
    <h2>{‌{user_profile.email}}</h2>
    <h2>{‌{user_profile.phone}}</h2>
    <hr/>
    <br/>
    <p>Summary</p>
    <p>{‌{user_profile.summary}}</p>
    <hr/>
    <p>Skills</p>
    <p>{‌{user_profile.skills}}</p>
    <hr/>
    <p>Education</p>
    <ul>
        <li>Schooling: {‌{user_profile.school}}</li>
        <li>{‌{user_profile.degree}} from {‌{user_profile.university}}</li>
    </ul>
    <hr/>
    <p>Previous Work</p>
    <p>{‌{user_profile.previous_work}}</p>
 
</body>
</html>
 
models py:
from django.db import models
 
# Create your models here.
class Profile(models.Model):
 
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    summary = models.TextField(max_length=2000)
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    previous_work = models.TextField(max_length=1000)
    skills = models.TextField(max_length=1000)
 
 
views py
 
from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
# Create your views here.
 
 
def accept(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work= request.POST.get("previous_work","")
        skills = request.POST.get("skills","")
 
        profile = Profile(name=name,email=email,phone=phone,summary=summary,degree=degree,school=school,university=university,previous_work=previous_work,skills=skills)
        profile.save()
 
    
    return render(request,'pdf/accept.html')
 
def resume(request,id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile':user_profile})
    options ={
        'page-size':'Letter',
        'encoding':"UTF-8",
    }
    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] ='attachment'
    filename = "resume.pdf"
    return response
 
def list(request):
    profiles = Profile.objects.all()
    return render(request,'pdf/list.html',{'profiles':profiles})
