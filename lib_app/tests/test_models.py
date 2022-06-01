from django.test import TestCase
from lib_app.models import Author, Genre, Book, Reading, Fine
# Create your tests here.


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(author_book='Достоевский Ф.М.', slug='dostoevskyfm')

    def test_author_verbose_name(self):
        author = Author.objects.get(pk=1)
        verbose_name = author._meta.get_field('author_book').verbose_name
        self.assertEqual(verbose_name, 'Автор')

    def test_author_max_length(self):
        author = Author.objects.get(pk=1)
        max_length = author._meta.get_field('author_book').max_length
        self.assertEqual(max_length, 80)

    def test_return_str(self):
        author = Author.objects.get(pk=1)
        author_book = 'Достоевский Ф.М.'
        self.assertEqual(str(author), author_book)
