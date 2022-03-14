from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from .models import Book, Author, Genre, Title

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


class Redaction(AllBooks):
    template_name = 'lib_app/redaction.html'

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


class CorrectBook(UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'lib_app/correct_book.html'


class CreateAuthor(CreateView):
    model = Author
    fields = '__all__'
    template_name = 'lib_app/create_item.html'

    def get_success_url(self, *args):
        return reverse_lazy('correct_book', args=(self.kwargs.get('pk'),))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_pk'] = self.kwargs.get('pk')
        context['action'] = 'create_author'
        return context


class CreateGenre(CreateAuthor):
    model = Genre

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create_genre'
        return context


class CorrectTitle(UpdateView):
    model = Title
    fields = '__all__'
    template_name = 'lib_app/correct_item.html'

    def get_success_url(self, *args):
        return reverse_lazy('correct_book', args=(self.kwargs.get('book_pk'),))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'correct_title'
        context['book_pk'] = self.kwargs.get('book_pk')
        return context


class CorrectAuthor(CorrectTitle):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'correct_author'
        return context


class CorrectGenre(CorrectTitle):
    model = Genre

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'correct_genre'
        return context
