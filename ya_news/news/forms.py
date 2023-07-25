from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Comment

"""
Часа три пытался сделать такую фичу:

response = requests.get(
    ('https://raw.githubusercontent.com/bars38/'
     'Russian_ban_words/master/words.txt')
)
BAD_WORDS = response.text

Но она ломает
test_authorized_client_can_create_comment:
Response code was 200 (expected 302)
Проблема в response. Причём response.close() не помог.
Поэтому сделал статичный файл.
"""

BAD_WORDS = tuple(
    word.replace('\n', '') for word in open('bad_words.txt').readlines()
)

WARNING = 'Не ругайтесь!'


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        """Не позволяем ругаться в комментариях."""
        text = self.cleaned_data['text']
        lowered_text = text.lower()
        for word in BAD_WORDS:
            if word in lowered_text:
                raise ValidationError(WARNING)
        return text
