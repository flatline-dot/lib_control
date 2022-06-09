from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from lib_app.models import Genre


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
