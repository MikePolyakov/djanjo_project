from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import RegistrationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import AppUser


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'users_app/login.html'


class UserCreateView(CreateView):
    model = AppUser
    template_name = 'users_app/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')


class PasswordResetByUser(PasswordChangeView):
    template_name = 'users_app/pass_change.html'
    success_url = reverse_lazy('users:login')
