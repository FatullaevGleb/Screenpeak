from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Title(models.Model):
    CATEGORY_CHOICES = [
        ('film', 'Фильм'),
        ('series', 'Сериал'),
        ('games', 'Игры'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория'
    )
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )
    description = models.TextField(
        max_length=1024,
        verbose_name='Описание',
        blank=True,
    )
    pub_year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(1888),
            MaxValueValidator(2030)
        ]
    )
    image = models.ImageField(
        'Постер',
        upload_to='titles/posters/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-pub_year',)

    def __str__(self):
        return self.title
