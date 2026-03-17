from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админ-панель для модели Review (Отзывы)"""

    list_display = (
        'author',
        'title',
        'rating',
        'created_at',
        'short_text',
    )
    list_editable = (
        'rating',
    )
    search_fields = (
        'text',
        'author__username',
        'title__title',
    )
    list_filter = ('rating', 'created_at', 'title__category')
    list_display_links = ('author', 'title')
    ordering = ('-created_at',)

    def short_text(self, obj):
        """Обрезает текст отзыва для отображения"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Текст отзыва'
