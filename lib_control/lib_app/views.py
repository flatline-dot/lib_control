from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView
from .models import Book, Author, Genre, Reading
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


class AllBooks(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
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


class ReaderList(ListView):
    template_name = 'lib_app/reader_list.html'

    def get_queryset(self):
        return User.objects.filter(groups__name='Reader')


class SelectReader(ReaderList):
    model = User
    template_name = 'lib_app/select_reader.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.kwargs['slug']
        print(context)
        return context


class ReaderCard(DetailView):
    model = User
    template_name = 'lib_app/reader_card.html'


class GiveConfirm(TemplateView):
    template_name = 'lib_app/give_confirm.html'

    def perm_valid(self):
        status = ''
        user = User.objects.get(pk=self.kwargs['pk'])
        book_id = Book.objects.get(slug=self.kwargs['slug']).pk
        if user.reading_set.count() >= 5:
            status = 'Пользователь читает 5 или более книг'
        elif Reading.objects.filter(book_id=book_id, user_id=user.pk).count():
            status = 'Пользователь уже читает эту книгу'

        return status if status else ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perm'] = self.perm_valid()
        context['book'] = Book.objects.get(slug=self.kwargs['slug'])
        context['user'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, **kwargs):
        book_id = Book.objects.get(slug=self.kwargs['slug'])
        user_id = User.objects.get(pk=self.kwargs['pk'])
        new_reading = Reading.objects.create(book_id=book_id, user_id=user_id, reading_days=10)
        new_reading.save()
        return redirect(reverse_lazy('reader_card', kwargs={'pk': self.kwargs['pk']}))

