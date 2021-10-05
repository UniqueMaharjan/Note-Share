from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import SubjectNote,SubjectList
from .forms import noteForm,listForm

def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User doesnot exit!!')
        user = authenticate(request, username = username, password = password)
    
        if user != None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"User or Password doesn't exist!!")
    content = {'page':page}
    return render(request,'note/login-register.html',content)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error')
    content = {
        'form':form
    }
    return render(request,'note/login-register.html',content)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = SubjectList.objects.all()
    notes = SubjectNote.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)
    )
    note_count = notes.count()
    content = {
        'note':notes,
        'topic':topics,
        'count':note_count,
    }
    return render(request,'note/home.html',content)

@login_required(login_url='login')
def noteDetails(request,pk):
    notes = SubjectNote.objects.get(id = pk)
    content = {
        'note':notes,
    }
    return render(request,'note/note.html',content)

@login_required(login_url='login')
def addNote(request):
    form = noteForm()
    if request.method == "POST":
        form = noteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'note/addnote.html',{'form':form})

def editNote(request,pk):
    note = SubjectNote.objects.get(id=pk)
    form = noteForm(instance=note)
    if request.method == "POST":
        form = noteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'note/addnote.html',{"form":form})

def deleteNote(request,pk):
    note = SubjectNote.objects.get(id=pk)
    if request.method == "POST":
        note.delete()
        return redirect('home')
    return render(request,'note/deletenote.html',{'obj':note})

def addTopic(request):
    form = listForm()
    if request.method == "POST":
        form = listForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'note/addtopic.html',{'form':form})