from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login_user
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login_user(request, user)
            return redirect('home')
    else:
        #form = UserCreationForm()
        form = SignUpForm()

    return render(request, 'signup.html', {'form':form})