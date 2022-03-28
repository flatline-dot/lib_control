from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import CreateUser


class RegisterUser(CreateView):
    form_class = CreateUser
    template_name = 'register.html'
    success_url = reverse_lazy('manage')
