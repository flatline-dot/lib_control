import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    author_book = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, allow_unicode=True, blank=True, unique=True, null=False)

    def __str__(self):
        return f'{self.author_book}'

    class Meta:
        ordering = ['author_book']


class Genre(models.Model):
    genre_book = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, allow_unicode=True, blank=True, unique=True, null=False)

    def __str__(self):
        return f'{self.genre_book}'

    class Meta:
        ordering = ['genre_book']


class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    book_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False)
    book_amount = models.IntegerField()
    slug = models.SlugField(max_length=50, allow_unicode=True, blank=True, unique=True, null=False)

    def available_count(self):
        return self.book_amount - self.reading_set.all().count() - self.reserve_set.all().count()

    def __str__(self):
        return f'{self.title}-{self.book_author}'

    def get_absolute_url(self):
        return reverse('correct_book', kwargs={'pk': self.pk})


    class Meta:
        ordering = ['title']


class Reading(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(auto_now_add=True, null=False)
    reading_days = models.IntegerField(null=False)
    fine = models.BooleanField(null=True)
    fine_date = models.DateField(null=True)

    def total_date(self):
        total_status = None
        #if (datetime.date(year=2022, month=5, day=15) - self.date_start).days > 10:
        if (datetime.date.today() - self.date_start).days > 10:
            total_status = 'Срок истек'

        elif (datetime.date.today() != self.date_start) and (datetime.date.today() - self.date_start).days == 0:
            total_status = 'Остался последний день'
        else:
            total_status = (self.date_start + datetime.timedelta(days=10) - datetime.date.today()).days

        return total_status

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

