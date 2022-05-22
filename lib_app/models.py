import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    author_book = models.CharField(max_length=50, unique=True, verbose_name='Автор')
    slug = models.SlugField(max_length=50, allow_unicode=True, blank=True, unique=True, null=False)

    def __str__(self):
        return f'{self.author_book}'

    class Meta:
        ordering = ['author_book']


class Genre(models.Model):
    genre_book = models.CharField(max_length=50, unique=True, verbose_name='Жанр')
    slug = models.SlugField(max_length=50, allow_unicode=True, blank=True, unique=True, null=False)

    def __str__(self):
        return f'{self.genre_book}'

    class Meta:
        ordering = ['genre_book']


class Book(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False, verbose_name='Автор')
    book_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False, verbose_name='Жанр')
    book_amount = models.IntegerField(verbose_name='Количество')
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

    def date_return(self):
        return self.date_start + datetime.timedelta(days=20)

    def __str__(self):
        return f'{self.book_id}, {self.user_id}'


class Fine(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reading_id = models.ForeignKey(Reading, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(null=False, auto_now_add=True)
    pay_status = models.BooleanField(null=False)
    pay_date = models.DateField(null=True, auto_now=True)

    def __str__(self):
        return f'{self.user_id}, {self.reading_id}, Оплачен: {self.pay_status}'

    class Meta:
        unique_together = ['user_id', 'reading_id']


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
