from django.apps import AppConfig


class UsersConfig(AppConfig):
    # Если используете Django 3.2+
    default_auto_field = 'django.db.models.BigAutoField'

    # Имя приложения - должно совпадать с именем папки
    name = 'users'

    # Человекочитаемое имя для админки (опционально)
    verbose_name = 'Пользователи'
