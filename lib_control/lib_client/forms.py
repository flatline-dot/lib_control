from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput, CharField


class CreateUser(UserCreationForm):
    password1 = CharField(label=("Password"), widget=PasswordInput(attrs={'class': 'form-input'}))
    password2 = CharField(label=("Password confirm"), widget=PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email',)
