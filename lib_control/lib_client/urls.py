from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('my_card/<int:pk>/', views.MyCard.as_view(), name='my_card')
]
