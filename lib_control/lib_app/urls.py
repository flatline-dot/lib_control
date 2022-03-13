from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllBooks.as_view(), name='home'),
    path('manage/', views.ManagementBooks.as_view(), name='manage'),
    path('redaction/', views.Redaction.as_view(), name='redaction'),
    path('correct_book/<int:pk>/', views.CorrectBook.as_view(), name='correct_book'),
    path('create_author/<int:pk>', views.CreateAuthor.as_view(), name='create_author'),
    path('create_genre/<int:pk>', views.CreateGenre.as_view(), name='create_genre'),
    path('correct_title<int:pk>', views.CorrectTitle.as_view(), name='correct_title'),
]
