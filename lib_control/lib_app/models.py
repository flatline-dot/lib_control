from django.db import models
from django.contrib.auth.models import User


class Title(models.Model):
    name_book = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name_book}'

    class Meta:
        ordering = ['name_book']


class Author(models.Model):
    author_book = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.author_book}'

    class Meta:
        ordering = ['author_book']


class Genre(models.Model):
    genre_book = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.genre_book}'

    class Meta:
        ordering = ['genre_book']


class Book(models.Model):
    book_title = models.ForeignKey(Title, on_delete=models.CASCADE, null=False)
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    book_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False)
    book_amount = models.IntegerField()

    def available_count(self):
        return self.book_amount - self.reading_set.all().count() - self.reserve_set.all().count()

    def __str__(self):
        return f'{self.book_title}-{self.book_author}'

    class Meta:
        ordering = ['book_title']


class Reading(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(auto_now_add=True, null=False)
    reading_days = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.book_id}, {self.user_id}'


class Reserve(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(auto_now_add=True, null=False)
    reserve_days = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.book_id}, {self.user_id}'


class Ban(models.Model):
    reading_id = models.ForeignKey(Reading, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    task = models.CharField(max_length=30, null=False)
    complete = models.BooleanField()

    def __str__(self):
        return f'{self.reading_id}, {self.user_id}'
