from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpRequest
from .forms import UserSignUpForm,UserLoginForm
from .models import User
from django.contrib.auth.hashers import make_password,check_password

def signup(request: HttpRequest):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created")
            return redirect("/")
        else:
            messages.warning(request, "invalid inputs!")
    form = UserSignUpForm()
    context = {"title": "Sign Up", "form": form}
    return render(request, "signup.html", context)


def login(request: HttpRequest):
    if request.session.exists('user_id'):
        return redirect('/home/')
    if request.method == 'POST':
        form= UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            if user:
                if check_password(form.cleaned_data['password'],  user.password):
                    request.session['user_id'] = user.id
                    return redirect('/home/')
    form = UserLoginForm()
    context={
        'title': 'Login',
        'form': form
    }
    return render(request, 'login.html',context)

def forgot_password(request: HttpRequest):
    pass

def home(request):
    return render(request, "home.html", {"title": "Home"})
