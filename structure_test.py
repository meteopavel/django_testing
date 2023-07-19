import sys
from collections import namedtuple
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(BASE_DIR)

PathForTests = namedtuple('TestPaths', ('rel_path', 'abs_path'))

ya_note_tests = BASE_DIR / 'ya_note/notes/tests/'
ya_news_tests = BASE_DIR / 'ya_news/news/pytest_tests/'

message_template = (
    '\nНе обнаружены тесты для проекта `{project}`. Убедитесь, что тесты, '
    'которые вы написали, размещены в директории `{path}`.'
)

projects_map = {
    'ya_note': PathForTests(
        'django_testing/ya_note/notes/tests', ya_note_tests
    ),
    'ya_news': PathForTests(
        'django_testing/ya_news/news/pytest_tests', ya_news_tests
    )
}

errors = []
for project_name, path in projects_map.items():
    if not path.abs_path.is_dir():
        errors.append(message_template.format(
            project=project_name, path=path.rel_path
        ))
        continue
    path_content = [obj for obj in path.abs_path.glob('*.py') if obj.is_file()]
    if not path_content:
        errors.append(message_template.format(
            project=project_name, path=path.rel_path
        ))


assert not errors, ''.join(errors)
