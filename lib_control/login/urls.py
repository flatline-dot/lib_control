from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login')
]