from django.contrib import admin

from .models import Title


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
    prepopulated_fields = {'slug': ('title',)}
