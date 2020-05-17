from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy, reverse
from .models import AppUser
from rest_framework.authtoken.models import Token


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


class UserDetailView(DetailView):
    model = AppUser
    template_name = 'users_app/profile.html'


def update_user_token(request):
    user = request.user
    # если уже есть
    if user.auth_token:
        # обновить
        user.auth_token.delete()
        Token.objects.create(user=user)
    else:
        # создать
        Token.objects.create(user=user)
    return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': user.pk}))
