from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'


@pytest.mark.django_db
def test_anonymous_client_cant_create_comment(client, another_news):
    """Тестируем пункт 1."""
    url = reverse('news:detail', args=(another_news.id,))
    form_data = {'text': COMMENT_TEXT}
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_authorized_client_can_create_comment(admin_client, another_news):
    """Тестируем пункт 2."""
    url = reverse('news:detail', args=(another_news.id,))
    form_data = {'text': COMMENT_TEXT}
    response = admin_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == another_news
    assert comment.author.username == 'admin'


def test_user_cant_use_bad_words(admin_client, another_news):
    """Тестируем пункт 3."""
    url = reverse('news:detail', args=(another_news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = admin_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(author_client, another_news, comment):
    """Тестируем пункт 4 часть 1"""
    edit_url = reverse('news:edit', args=(comment.id,))
    detail_url = reverse('news:detail', args=(another_news.id,)) + '#comments'
    form_data = {'text': COMMENT_TEXT}
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, detail_url)
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT


def test_author_can_delete_comment(author_client, another_news, comment):
    """Тестируем пункт 4 часть 2"""
    delete_url = reverse('news:delete', args=(comment.id,))
    detail_url = reverse('news:detail', args=(another_news.id,)) + '#comments'
    response = author_client.delete(delete_url)
    assertRedirects(response, detail_url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_authorized_client_cant_edit_comment_of_another_user(
        admin_client, comment
):
    """Тестируем пункт 5 часть 1"""
    edit_url = reverse('news:edit', args=(comment.id,))
    form_data = {'text': COMMENT_TEXT + 'addition'}
    response = admin_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT


def test_authorized_client_cant_delete_comment_of_another_user(
        admin_client, comment
):
    """Тестируем пункт 5 часть 2"""
    delete_url = reverse('news:delete', args=(comment.id,))
    response = admin_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
