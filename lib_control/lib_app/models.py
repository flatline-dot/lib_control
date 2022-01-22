from django.db import models
from django.contrib.auth.models import User


class Title(models.Model):
    name_book = models.CharField(max_length=50, unique=True)


class Author(models.Model):
    author_book = models.CharField(max_length=50, unique=True)


class Genre(models.Model):
    genre_book = models.CharField(max_length=50, unique=True)


class Book(models.Model):
    book_title = models.ForeignKey(Title, on_delete=models.CASCADE, null=False)
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    book_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False)
    book_amount = models.IntegerField()


class Reading(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(auto_now_add=True, null=False)
    reading_days = models.IntegerField(null=False)


class Reserve(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(auto_now_add=True, null=False)
    reserve_days = models.IntegerField(null=False)


class Ban(models.Model):
    reading_id = models.ForeignKey(Reading, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    task = models.CharField(max_length=30, null=False)
    complete = models.BooleanField()
