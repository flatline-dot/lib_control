import datetime
from django.test import TestCase
from lib_app.models import Author, Genre, Book, Reading, Fine
from django.contrib.auth.models import User
# Create your tests here.


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(author_book='Достоевский Ф.М.', slug='dostoevskyfm')

    def setUp(self):
        self.author = Author.objects.all()[0]

    def test_author_verbose_name(self):
        verbose_name = self.author._meta.get_field('author_book').verbose_name
        max_length = self.author._meta.get_field('author_book').max_length
        unique = self.author._meta.get_field('author_book').unique

        self.assertEqual(verbose_name, 'Автор')
        self.assertEqual(max_length, 80)
        self.assertTrue(unique)

    def test_return_str(self):
        author_book = 'Достоевский Ф.М.'
        self.assertEqual(str(self.author), author_book)


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(genre_book='Классика', slug='classika')

    def setUp(self):
        self.genre = Genre.objects.all()[0]

    def test_genre_verbose_name(self):
        verbose_name = self.genre._meta.get_field('genre_book').verbose_name
        max_length = self.genre._meta.get_field('genre_book').max_length
        unique = self.genre._meta.get_field('genre_book').unique

        self.assertEqual(verbose_name, 'Жанр')
        self.assertEqual(max_length, 80)
        self.assertTrue(unique)

    def test_genre_str(self):
        self.assertEqual(str(self.genre), 'Классика')


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(author_book='Достоевский Ф.М.', slug='dostoevskyfm')
        test_genre = Genre.objects.create(genre_book='Классика', slug='classika')
        test_user = User.objects.create(username='test_user')
        test_book = Book.objects.create(title='Преступление и наказание',
                                        book_author=test_author,
                                        book_genre=test_genre,
                                        book_amount=10,
                                        slug='prestupleniye_i_nakazanye'
                                        )

        test_reading = Reading.objects.create(book_id=test_book, user_id=test_user)
        test_fine = Fine.objects.create(user_id=test_user,
                                        reading_id=test_reading,
                                        pay_status=False,
                                        )

    def setUp(self):
        self.book = Book.objects.all()[0]

    def test_book_title(self):
        verbose_name = self.book._meta.get_field('title').verbose_name
        max_length = self.book._meta.get_field('title').max_length
        unique = self.book._meta.get_field('title').unique
        self.assertEqual(verbose_name, 'Название')
        self.assertEqual(max_length, 80)
        self.assertTrue(unique)

    def test_book_author(self):
        verbose_name = self.book._meta.get_field('book_author').verbose_name
        max_length = self.book._meta.get_field('book_author').max_length
        self.assertEqual(verbose_name, 'Автор')
        self.assertEqual(max_length, 80)

    def test_book_genre(self):
        verbose_name = self.book._meta.get_field('book_genre').verbose_name
        max_length = self.book._meta.get_field('book_genre').max_length
        self.assertEqual(verbose_name, 'Жанр')
        self.assertEqual(max_length, 80)

    def test_book_amount(self):
        verbose_name = self.book._meta.get_field('book_amount').verbose_name
        self.assertEqual(verbose_name, 'Количество')

    def test_book_slug(self):
        max_length = self.book._meta.get_field('slug').max_length
        self.assertEqual(max_length, 80)

    def test_available_count(self):
        available_count = self.book.available_count()
        self.assertEqual(available_count, 9)

    def test_str(self):
        self.assertEqual(str(self.book), 'Преступление и наказание-Достоевский Ф.М.')


class ReadingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        BookModelTest.setUpTestData()

    def setUp(self):
        self.reading = Reading.objects.all()[0]

    def test_date_return(self):
        date_return = self.reading.date_return()
        true_date = datetime.date.today() + datetime.timedelta(days=20)
        self.assertEqual(date_return, true_date)


class FineModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        BookModelTest.setUpTestData()

    def setUp(self):
        self.fine = Fine.objects.all()[0]

    def test_fine_str(self):
        self.assertEqual(str(self.fine), 'Преступление и наказание-Достоевский Ф.М., test_user, Оплачен: False')
