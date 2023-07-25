import pytest
from django.conf import settings
from django.urls import reverse

from conftest import HOME_PAGE
from news.forms import CommentForm


def get_object_list(client, news_for_home_page):
    url = reverse(HOME_PAGE)
    response = client.get(url)
    object_list = response.context['object_list']
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
    all_comments = response.context['news'].comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, another_news):
    """Тестируем пункт 4 часть 1."""
    url = reverse('news:detail', args=(another_news.id,))
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(admin_client, another_news):
    """Тестируем пункт 4 часть 2."""
    url = reverse('news:detail', args=(another_news.id,))
    response = admin_client.get(url)
    assert (
        'form' in response.context
        and isinstance(response.context['form'], CommentForm)
    )
