from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import logout, login
# Create your views here.
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('/book/')
        else:
            print(form.errors)
        return render(request,'login.html', {"form":form})
class RegisterView(View):
    
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save in db
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/login/')
        else:
            print(form.errors)
        return render(request, 'register.html', {'form': form})

