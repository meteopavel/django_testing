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
        cls.auth_user_urls = (
            ('/'), ('/add/'), ('/notes/'), ('/done/')
        )
        cls.edit_delete_urls = (
            ('/note/'), ('/edit/'), ('/delete/')
        )
        """С этим промучился часов 5, так как многое мешает.
        Конечно, это были полезные часы, многое закрепил о поведении
        разных коллекций и об их методах.
        В итоге решение работает, но мне это видится костылем.
        """
        cls.redirect_urls = list(cls.auth_user_urls + cls.edit_delete_urls)
        cls.redirect_urls = [
            [cls.redirect_urls[i][:-1]]
            for i in range(1, len(cls.redirect_urls))
        ]
        for i in range(len(cls.redirect_urls)):
            (cls.redirect_urls[i].insert(1, 'slug') if i > 2 else
             cls.redirect_urls[i].insert(1, ''))

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
        urls = self.auth_user_urls
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
            for name in self.edit_delete_urls:
                with self.subTest():
                    url = f'{name}{self.note.slug}/'
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Тестируем пункт 4."""
        login_url = '/auth/login/'
        urls = self.redirect_urls
        for name, args in urls:
            with self.subTest():
                url = f'{name}/{args.replace("slug", self.note.slug + "/")}'
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
