from django.contrib import admin

from .models import Book, Title, Genre, Author


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
