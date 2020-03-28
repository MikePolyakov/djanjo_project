from django.contrib.auth.forms import UserCreationForm
from .models import AppUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ('username', 'password1', 'password2', 'email')