from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return HttpResponseRedirect(reverse('index'))

    return render(request, 'register.html', context={'form': form})

def login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return HttpResponseRedirect(reverse('index'))

    return render(request, 'login.html', context={'form': form})

def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('login'))