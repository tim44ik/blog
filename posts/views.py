from django.shortcuts import render,redirect
from .models import Post
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request,'index.html',{'posts':posts})

def post(request,pk):
    posts = Post.objects.get(id=pk)
    return render(request,'post.html', {'posts':posts})

def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        created_at = datetime.now()
        post = Post(title=title, body=text, created_at=created_at)
        post.save()
        return redirect('/') 
    else:
        return render(request, 'create_post.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email is already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username is already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user = auth.authenticate(username=username, password=password)
                auth.login(request,user)
                return redirect('/')
        else:
            messages.info(request, 'Passwords must be equal')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
        
        users = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
        if users.exists():
            user = users.first()
            if user.check_password(password):
                auth.login(request, user)
                return redirect('/')
            
        messages.info(request, 'Data you are providing is incorrect')
        return redirect('login')
    else:
        return render(request, 'login.html')

def remove(request,pk):
    Post.objects.get(id=pk).delete()
    return redirect('/')

def edit(request,pk):
    if request.method == 'POST':
        post = Post.objects.get(id=pk)
        post.title = request.POST['title']
        post.body = request.POST['text']
        post.created_at = datetime.now()
        post.save()
        return redirect('index') 
    else:
        return render(request, 'edit.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
