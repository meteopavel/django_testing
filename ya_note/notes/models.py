from django.conf import settings
from django.db import models

from pytils.translit import slugify


class Note(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=100,
        default='Название заметки',
        help_text='Дайте короткое название заметке'
    )
    text = models.TextField(
        'Текст',
        help_text='Добавьте подробностей'
    )
    slug = models.SlugField(
        'Адрес для страницы с заметкой',
        max_length=100,
        unique=True,
        blank=True,
        help_text=('Укажите адрес для страницы заметки. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            max_slug_length = self._meta.get_field('slug').max_length
            self.slug = slugify(self.title)[:max_slug_length]
        super().save(*args, **kwargs)
