from django.contrib import admin
from .models import Title, Review


admin.site.empty_value_display = 'Не задано'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админ-панель для модели Title (Произведения)"""

    list_display = (
        'title',
        'category',
        'pub_year',
        'slug',
    )
    list_editable = (
        'category',
        'pub_year',
    )
    search_fields = (
        'title',
        'description',
    )
    list_filter = ('category',)
    list_display_links = ('title',)
    ordering = ('-pub_year',)

    # Автозаполнение slug из названия (удобно!)
    prepopulated_fields = {'slug': ('title',)}

    # Показываем только первые 50 символов описания в поиске
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        return queryset, use_distinct


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админ-панель для модели Review (Отзывы)"""

    list_display = (
        'title',
        'author',
        'rating',
        'created_at',
    )
    list_editable = (
        'rating',
    )
    search_fields = (
        'text',
        'author__username',
        'title__title',
    )
    list_filter = ('rating', 'created_at')
    list_display_links = ('title',)
    ordering = ('-created_at',)
