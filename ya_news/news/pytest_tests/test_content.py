import re

import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm
from news.models import Comment

HOME_PAGE = ('news:home')


def get_object_list(client, news_for_home_page):
    response = client.get(reverse(HOME_PAGE))
    object_list = response.context.get('object_list')
    if object_list is not None:
        return object_list


@pytest.mark.django_db
def test_news_count(client, news_for_home_page):
    """Тестируем пункт 1."""
    object_list = get_object_list(client, news_for_home_page)
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_for_home_page):
    """Тестируем пункт 2."""
    object_list = get_object_list(client, news_for_home_page)
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, another_news_with_comments):
    """Тестируем пункт 3."""
    url = reverse('news:detail', args=(another_news_with_comments.id,))
    response = client.get(url)
    comments_from_page = response.content.decode('utf-8')
    comments_from_db = Comment.objects.values('text').order_by('created')
    comments_list = [comment['text'] for comment in comments_from_db]
    comments_list_pattern = re.compile(r'[\s\S]+?'.join(comments_list))
    assert re.search(comments_list_pattern, comments_from_page)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, base_news_detail_url):
    """Тестируем пункт 4 часть 1."""
    response = client.get(base_news_detail_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(admin_client, base_news_detail_url):
    """Тестируем пункт 4 часть 2."""
    response = admin_client.get(base_news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
