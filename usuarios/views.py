from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .decorators import user_not_authenticated

# Create your views here.
@user_not_authenticated
def register(request):
    # Logged in user can't register a new account
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Nuevo usuario registrado: {user.username}")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request = request,
        template_name = "users/register.html",
        context={"form":form}
        )

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Has salido de tu sesión")
    return redirect("login")

@user_not_authenticated
def custom_login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hola <b>{user.username}</b>! Has iniciado sesión")
                return redirect('panel')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = AuthenticationForm() 
    
    return render(
        request=request,
        template_name="users/login.html", 
        context={'form': form}
        )

def signup_redirect(request):
    messages.error(request, "Has iniciado sesión con google, sin embargo los contenidos no se pueden ver con google!")
    return redirect("homepage")