from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

User = get_user_model()


@pytest.fixture
def unlogged_client(client):
    return client


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def another_news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def base_news_url(another_news):
    return f'/news/{another_news.id}/'


@pytest.fixture
def base_news_detail_url(another_news):
    return reverse('news:detail', args=(another_news.id,))


@pytest.fixture
def news_for_home_page():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(author, another_news):
    return Comment.objects.create(
        news=another_news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def another_news_with_comments(author, another_news):
    another_news_with_comments = another_news
    now = timezone.now()
    for index in range(3):
        comment = Comment.objects.create(
            news=another_news_with_comments,
            author=author,
            text=f'Tекст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return another_news_with_comments
