from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

LAZY_ADMIN = pytest.lazy_fixture('admin_client')
LAZY_AUTHOR = pytest.lazy_fixture('author_client')
LAZY_NEWS_URL = pytest.lazy_fixture('base_news_url')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('/', '/auth/login/', '/auth/logout/', '/auth/signup/', LAZY_NEWS_URL)
)
def test_pages_availability_for_anonymous_user(client, name):
    """Тестируем пункты 1, 2 и 6."""
    response = client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        ('/edit_comment/', LAZY_ADMIN, HTTPStatus.NOT_FOUND),
        ('/delete_comment/', LAZY_ADMIN, HTTPStatus.NOT_FOUND),
        ('/edit_comment/', LAZY_AUTHOR, HTTPStatus.OK),
        ('/delete_comment/', LAZY_AUTHOR, HTTPStatus.OK),
    ),
)
def test_comments_availability_for_different_users(
        name, parametrized_client, expected_status, comment
):
    """Тестируем пункты 3 и 5."""
    url = f'{name}{comment.id}/'
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, comment_object',
    (
        ('/edit_comment/', pytest.lazy_fixture('comment')),
        ('/delete_comment/', pytest.lazy_fixture('comment')),
    ),
)
def test_redirects_for_anonymous_user(client, name, comment_object):
    """Тестируем пункт 4."""
    login_url = '/auth/login/'
    url = f'{name}{comment_object.id}/'
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
