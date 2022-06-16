from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from lib_app.models import Genre, Author, Book


class AllBookTestView(TestCase):

    @classmethod
    def setUpTestData(cls):
        manager_group = Group.objects.create(name='Manager')
        reader_group = Group.objects.create(name='Reader')
        perm = Permission.objects.filter(codename='view_book').first()
        manager_group.permissions.add(perm)

        reader = User.objects.create(username='ReaderUser')
        manager = User.objects.create(username='ManagerUser')
        manager.set_password('12345678')
        reader.set_password('12345')
        manager.save()
        reader.save()

        reader.groups.add(reader_group)
        manager.groups.add(manager_group)

        genre_first = Genre.objects.create(genre_book='Русская классика', slug='russkaya_classika')
        genre_second = Genre.objects.create(genre_book='Зарубежное', slug='zarybejnoe')

        author_first = Author.objects.create(author_book='Достоевский Ф.М.', slug='dostoevskiy_fm')
        author_second = Author.objects.create(author_book='Джек Лондон', slug='jack_london')

        book_first = Book.objects.create(title='Преступление и наказание',
                                         book_author=author_first,
                                         book_genre=genre_first, book_amount=10,
                                         slug='prestuplenie_i_nakazanie')

        book_second = Book.objects.create(title='Бесы',
                                          book_author=author_first,
                                          book_genre=genre_first, book_amount=15,
                                          slug='besy')

        book_third = Book.objects.create(title='Белый клык',
                                         book_author=author_second,
                                         book_genre=genre_second, book_amount=20,
                                         slug='beluy_kluk')

    def setUp(self):
        self.client = Client()

    def test_anonymous_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/')

    def test_reader_user(self):
        self.client.login(username='ReaderUser', password='12345')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 403)

    def test_manager_user(self):
        self.client.login(username='ManagerUser', password='12345678')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'lib_app/all_books.html')

        search_response = self.client.get('/?search_select=title&search_query=Преступление и наказание')
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(search_response.templates[0].name, 'lib_app/all_books.html')
        self.assertEqual(str(search_response.context['object_list'][0]), 'Преступление и наказание-Достоевский Ф.М.')
        self.assertEqual(len(search_response.context['object_list']), 1)
