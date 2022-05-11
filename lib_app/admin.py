from django.contrib import admin

from .models import Book, Fine, Genre, Author, Reading


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Reading)
admin.site.register(Fine)
