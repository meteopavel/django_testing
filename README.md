# Django testing  
## Если вы успели выполнить все домашние задания — ваш финальный проект готов.
Перенесите тесты из ваших проектов в данный репозиторий (**django_testing**), который появился в вашем аккаунте.  
В итоге должна получиться следующая структура репозитория:
```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с вашими тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с вашими тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```

## После копирования тестов, написанных в ходе прохождения спринта, для проверки готовности проекта к сдаче необходимо выполнить 4 действия:
1. Создать и активировать виртуальное окружение; установить зависимости из файла `requirements.txt`;
2. Запустить скрипт для `run_tests.sh` из корневой директории проекта:
```sh
bash run_tests.sh
```

**Если все проверки успешно выполнились, проект можно отправлять на ревью.**
