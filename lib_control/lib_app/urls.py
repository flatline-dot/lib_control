from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllBooks.as_view(), name='home'),
    path('manage/', views.ManagementBooks.as_view(), name='manage'),
    path('redaction/', views.Redaction.as_view(), name='redaction'),
    path('correct_book/<slug:slug>/', views.CorrectBook.as_view(), name='correct_book'),
    path('create_author/', views.CreateAuthor.as_view(), name='create_author'),
    path('create_genre/', views.CreateGenre.as_view(), name='create_genre'),
    path('correct_author/<slug:slug>/', views.CorrectAuthor.as_view(), name='correct_author'),
    path('correct_genre/<slug:slug>/', views.CorrectGenre.as_view(), name='correct_genre'),
    path('replenishment/', views.NewBook.as_view(), name='new_book'),
    path('choice_user/', views.UserList.as_view(), name='choice_user'),
    path('readers/', views.ReaderList.as_view(), name='readers'),
    path('reader_card/<int:pk>/', views.ReaderCard.as_view(), name='reader_card')

]
