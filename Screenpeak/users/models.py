from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    # Уже есть в AbstractUser: username, email, first_name, last_name, password, groups, etc.

    # Добавляем:
    bio = models.TextField('О себе', max_length=500, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    # Для будущих фич:
    email_verified = models.BooleanField('Email подтвержден', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
