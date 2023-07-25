from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

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

    def test_note_in_list_for_different_users(self):
        """Тестируем пункты 1 и 2."""
        notes_statuses_for_users = (
            (self.author, True),
            (self.authenticated_user, False),
        )
        for user, note_in_list in notes_statuses_for_users:
            self.client.force_login(user)
            with self.subTest(user=user):
                response = self.client.get(reverse('notes:list'))
                self.assertEqual(
                    self.note in response.context['object_list'],
                    note_in_list
                )

    def test_create_and_edit_note_pages_contains_form(self):
        """Тестируем пункт 3."""
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest():
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
