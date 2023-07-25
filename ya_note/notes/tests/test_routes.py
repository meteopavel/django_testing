from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.authenticated_user = User.objects.create(
            username='Аутентифицированный пользователь'
        )
        cls.author = User.objects.create(
            username='Автор заметки'
        )
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_pages_availability_for_anonymous_user(self):
        """Тестируем пункты 1 и 5."""
        urls = (
            (''),
            ('/auth/login/'),
            ('/auth/logout/'),
            ('/auth/signup/'),
        )
        for name in urls:
            with self.subTest():
                url = name
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_authenticated_user(self):
        """Тестируем пункт 2."""
        urls = (
            (''),
            ('/add/'),
            ('/notes/'),
            ('/done/'),
        )
        self.client.force_login(self.authenticated_user)
        for name in urls:
            with self.subTest():
                url = name
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_edit_and_delete(self):
        """Тестируем пункт 3."""
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.authenticated_user, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (
                '/note/',
                '/edit/',
                '/delete/'
            ):
                with self.subTest():
                    url = f'{name}{self.note.slug}/'
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Тестируем пункт 4."""
        login_url = '/auth/login/'
        urls = (
            ('/add', ''),
            ('/notes', ''),
            ('/done', ''),
            ('/edit/', (self.note.slug)),
            ('/note/', (self.note.slug)),
            ('/delete/', (self.note.slug)),
        )
        for name, args in urls:
            with self.subTest():
                url = f'{name}{args}/'
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
