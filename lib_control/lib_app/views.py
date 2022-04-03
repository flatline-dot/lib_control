from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from .models import Book, Author, Genre
from transliterate import translit


sort_options = {
    'title': 'Книги по алфавиту',
    '-title': 'Книги в обратном порядке',
    'book_author': 'Авторы по алфавиту',
    '-book_author': 'Авторы в обратном порядке',
    'book_genre': 'Жанры по алфавиту',
    '-book_genre': 'Жанры в обратном порядке'
}

search_options = {
    'title': 'По книгам',
    'book_author': 'По авторам',
    'book_genre': 'По жанрам'
}

make_queries = {
    'title': 'title',
    'book_author': 'book_author__author_book',
    'book_genre': 'book_genre__genre_book',
}


class AllBooks(ListView):
    model = Book
    template_name = 'lib_app/all_books.html'


class ManagementBooks(TemplateView):
    template_name = 'lib_app/management.html'


class Redaction(PermissionRequiredMixin, AllBooks):
    template_name = 'lib_app/redaction.html'
    permission_required = 'lib_app.view_book'

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
    fields = ['title', 'book_author', 'book_genre', 'book_amount']
    template_name = 'lib_app/correct_book.html'
    success_url = reverse_lazy('redaction')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.slug = slugify(translit(instance.title, reversed=True), allow_unicode=True)
        instance.save()
        return redirect(self.get_success_url())


class CorrectAuthor(UpdateView):
    model = Author
    fields = ['author_book']
    template_name = 'lib_app/correct_item.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(translit(self.object.author_book, reversed=True))
        self.object.save()
        slug = self.object.slug
        return redirect(self.get_success_url(slug))

    def get_success_url(self, *args):
        return reverse_lazy('correct_author', args=args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'correct_author'
        return context


class CorrectGenre(CorrectAuthor):
    model = Genre
    fields = ['genre_book']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(translit(self.object.genre_book, reversed=True))
        self.object.save()
        slug = self.object.slug
        return redirect(self.get_success_url(slug))

    def get_success_url(self, *args):
        return reverse_lazy('correct_genre', args=args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'correct_genre'
        return context


class CreateAuthor(CreateView):
    model = Author
    fields = ['author_book']
    template_name = 'lib_app/create_item.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(translit(self.object.author_book, reversed=True))
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self, *args):
        return reverse_lazy('create_author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create_author'
        return context


class CreateGenre(CreateAuthor):
    model = Genre
    fields = ['genre_book']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(translit(self.object.genre_book, reversed=True))
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self, *args):
        return reverse_lazy('create_genre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create_genre'
        return context


class NewBook(CreateView):
    model = Book
    fields = ['title', 'book_author', 'book_genre', 'book_amount']
    template_name = 'lib_app/new_book.html'
    success_url = reverse_lazy('manage')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(translit(self.object.title, reversed=True), allow_unicode=True)
        self.object.save()
        return redirect(self.get_success_url())

