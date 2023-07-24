from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель простой')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='note-slug',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        users = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        url = reverse('notes:list')
        for user, value in users:
            with self.subTest(user=user):
                object_list = user.get(url).context['object_list']
                self.assertTrue((self.note in object_list) is value)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for page, args in urls:
            with self.subTest(page=page):
                url = reverse(page, args=args)
                response = self.author_client.get(url)
                assert ('form' in response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
