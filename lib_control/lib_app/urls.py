from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllBooks.as_view(), name='home'),
    path('manage/', views.ManagementBooks.as_view(), name='manage'),
    path('correct/', views.CorrectBooksData.as_view(), name='correct')
]
