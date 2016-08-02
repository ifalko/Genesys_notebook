from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('content:list_record')
        else:
            return render(request, 'login.html', {
              	'login_error': "* User not found",
              })
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('loginsys:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
