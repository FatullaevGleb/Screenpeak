from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Title(models.Model):
    category = models.CharField(
        max_length=20,
        choices=[
            ('film', 'Фильм'),
            ('series', 'Сериал'),
            ('anime', 'Аниме')
        ],
        verbose_name='Категория'
    )
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'),
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
        default_related_name = 'title'

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )
    text = models.TextField(
        max_length=2056,
        verbose_name='Текст отзыва'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Минимальная оценка - 1'),
            MaxValueValidator(10, message='Максимальная оценка - 10')
        ],
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at',)
        default_related_name = 'review'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title_review'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'
