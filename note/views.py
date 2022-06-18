from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import SubjectNote, SubjectList, User
from .forms import noteForm, MyUserCreationForm, MyUserForm


def login_user(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User doesnot exit!!")
        user = authenticate(request, email=email, password=password)

        if user != None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "User or Password doesn't exist!!")
    content = {"page": page}
    return render(request, "note/login-register.html", content)


def logout_user(request):
    logout(request)
    return redirect("home")


def register_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop("confirm_password")
            User.objects.create(**form.cleaned_data)
            return redirect("login")
        else:
            messages.error(
                request,
                "Please Checkout your passwords.... Try to implement strong one . .",
            )
    content = {"form": form}
    return render(request, "note/login-register.html", content)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = SubjectList.objects.all()
    notes = SubjectNote.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(host__email__icontains=q)
    )
    note_count = notes.count()
    content = {
        "note": notes,
        "topic": topics,
        "count": note_count,
    }
    return render(request, "note/home.html", content)


@login_required(login_url="login")
def noteDetails(request, pk):
    notes = SubjectNote.objects.get(id=pk)
    content = {
        "note": notes,
    }
    return render(request, "note/note.html", content)


@login_required(login_url="login")
def addNote(request):
    form = noteForm()
    topic = SubjectList.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = SubjectList.objects.get_or_create(name=topic_name)

        SubjectNote.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            body=request.POST.get("body"),
            file_upload=request.FILES.get("file_upload"),
        )
        return redirect("home")
    return render(request, "note/create.html", {"form": form, "topic": topic})


@login_required(login_url="login")
def editNote(request, pk):
    note = SubjectNote.objects.get(id=pk)
    form = noteForm(instance=note)
    topic = SubjectList.objects.all()
    if request.user != note.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = SubjectList.objects.get_or_create(name=topic_name)
        note.name = request.POST.get("name")
        note.topic = topic
        note.body = request.POST.get("body")
        note.file_upload = request.FILES.get("file_upload")
        note.save()
        return redirect("home")
    return render(request, "note/create.html", {"form": form, "topic": topic})


@login_required(login_url="login")
def deleteNote(request, pk):
    note = SubjectNote.objects.get(id=pk)
    if request.method == "POST":
        note.delete()
        return redirect("home")
    return render(request, "note/delete.html", {"obj": note})


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    note = user.subjectnote_set.all()
    context = {"user": user, "note": note}
    return render(request, "note/user-profile.html", context)


def updateUser(request):
    user = User.objects.get(email=request.user.email)
    form = MyUserForm(instance=user)
    if request.method == "POST":
        form = MyUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {
        "form": form,
    }
    return render(request, "note/update-user.html", context)


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topic = SubjectList.objects.filter(name__icontains=q)
    return render(request, "note/topics.html", {"topics": topic})
