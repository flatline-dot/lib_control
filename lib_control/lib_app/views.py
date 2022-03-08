from django.views.generic import ListView, TemplateView
from .models import Book

sort_options = {
    'book_title': 'Книги по алфавиту',
    '-book_title': 'Книги в обратном порядке',
    'book_author': 'Авторы по алфавиту',
    '-book_author': 'Авторы в обратном порядке',
    'book_genre': 'Жанры по алфавиту',
    '-book_genre': 'Жанры в обратном порядке'
}

class AllBooks(ListView):
    model = Book
    template_name = 'lib_app/all_books.html'


class ManagementBooks(TemplateView):
    template_name = 'lib_app/management.html'


class CorrectBooksData(AllBooks):
    template_name = 'lib_app/correct_books_data.html'

    def get_ordering(self):
        ordering = self.request.GET.get('select')
        print(self.request.GET)
        return ordering

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_options'] = sort_options
        context['choice_sort_options'] = self.request.GET.get('select')
        return context
