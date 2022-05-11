from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import Group
from .forms import CreateUser
from django.contrib.auth.models import User


class RegisterUser(CreateView):
    form_class = CreateUser
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        group = Group.objects.get(pk=2)
        self.object.groups.add(group)
        return super().form_valid(form)


class MyCard(DetailView):
    template_name = 'my_card.html'
    model = User
