from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html')

def auth(request):
    return render(request, 'auth.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_portal')
    else:
        form = UserCreationForm()
    return render(request, 'auth.html', {'form': form, 'form_type': 'signup'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_portal')
    else:
        form = AuthenticationForm()
    return render(request, 'auth.html', {'form': form, 'form_type': 'login'})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def user_portal(request):
    return render(request, 'user_portal.html', {'username': request.user.username})


