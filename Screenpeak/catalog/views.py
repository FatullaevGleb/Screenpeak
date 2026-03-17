from django.contrib.auth.mixins import LoginRequiredMixin  # добавь эту строку
from django.views.generic import ListView

from reviews.models import Review

from .models import Title


class TitleListView(LoginRequiredMixin, ListView):
    """
    Список произведений, на которые пользователь оставил отзывы.
    Только для авторизованных пользователей.
    """
    model = Title
    template_name = 'catalog/title_list.html'
    paginate_by = 10
    context_object_name = 'titles'

    def get_queryset(self):

        category = self.kwargs.get('category', 'film')

        reviewed_title_ids = Review.objects.filter(
            author=self.request.user,
            title__category=category
        ).values_list('title_id', flat=True)

        return Title.objects.filter(
            id__in=reviewed_title_ids
        ).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('category')
        return context

    def handle_no_permission(self):
        """Если пользователь не авторизован - редирект на главную"""
        from django.shortcuts import redirect
        return redirect('home')
