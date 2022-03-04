from django.views.generic import ListView
from .models import Book
from django.views import View

class AllBooks(ListView):
    model = Book
    template_name = 'lib_app/all_books.html'

