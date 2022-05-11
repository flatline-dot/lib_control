from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from . import views
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]