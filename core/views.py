from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Invalid Crednetials")
            return redirect("login")
    else:
        return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken!")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken!")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect("/")

        else:
            messages.info(request, "Password Not Matching!")
            return redirect("signup")

    else:
        return render(request, "signup.html")
