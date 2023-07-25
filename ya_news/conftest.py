from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from news.models import Comment, News

User = get_user_model()

HOME_PAGE = 'news:home'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def another_news():
    another_news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return another_news


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
    return news_for_home_page


@pytest.fixture
def comment(author, another_news):
    comment = Comment.objects.create(
        news=another_news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def another_news_with_comments(author, another_news):
    another_news_with_comments = another_news
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=another_news_with_comments,
            author=author,
            text=f'Tекст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return another_news_with_comments
