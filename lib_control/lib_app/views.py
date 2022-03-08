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

search_options = {
    'book_title': 'По книгам',
    'book_author': 'По авторам',
    'book_genre': 'По жанрам'
}

make_queries = {
    'book_title': 'book_title__name_book',
    'book_author': 'book_author__author_book',
    'book_genre': 'book_genre__genre_book',
}


class AllBooks(ListView):
    model = Book
    template_name = 'lib_app/all_books.html'


class ManagementBooks(TemplateView):
    template_name = 'lib_app/management.html'


class CorrectBooksData(AllBooks):
    template_name = 'lib_app/correct_books_data.html'

    def get_queryset(self):
        queryset = True
        if self.request.GET.get('search_query') and self.request.GET.get('search_select'):
            field_ = make_queries[self.request.GET.get('search_select')]
            search_data = self.request.GET.get('search_query')
            queryset = Book.objects.filter(**{field_: search_data})

        else:
            queryset = Book.objects.all()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def get_ordering(self):
        ordering = self.request.GET.get('select')
        return ordering

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_options'] = sort_options
        context['choice_sort_options'] = self.request.GET.get('select')
        context['search_options'] = search_options
        context['choice_search_options'] = self.request.GET.get('search_select')
        context['search_query'] = self.request.GET.get('search_query')
        return context
