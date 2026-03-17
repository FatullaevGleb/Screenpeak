from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from catalog.models import Title

from .forms import ReviewForm
from .models import Review


class MyReviewsView(LoginRequiredMixin, ListView):
    """Страница со всеми отзывами пользователя"""
    model = Review
    template_name = 'reviews/my_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(
            author=self.request.user
        ).select_related('title').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои отзывы'
        return context


class AddReviewView(LoginRequiredMixin, CreateView):
    """Добавление нового отзыва"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:my_reviews')

    def generate_slug(self, title):
        """Генерирует уникальный slug из названия"""
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Title.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def form_valid(self, form):
        title_name = form.cleaned_data['title_name']
        category = form.cleaned_data['category']

        title, created = Title.objects.get_or_create(
            title=title_name,
            defaults={
                'category': category,
                'slug': self.generate_slug(title_name),
                'pub_year': 2000,
                'description': '',
            }
        )

        if not created and title.category != category:
            title.category = category
            title.save()

        form.instance.author = self.request.user
        form.instance.title = title

        messages.success(self.request, 'Отзыв успешно добавлен!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить отзыв'
        context['button_text'] = 'Опубликовать'
        return context


class EditReviewView(LoginRequiredMixin, UpdateView):
    """Редактирование отзыва"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:my_reviews')

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)

    def generate_slug(self, title):
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Title.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def form_valid(self, form):
        title_name = form.cleaned_data['title_name']
        category = form.cleaned_data['category']
        current_review = self.get_object()

        if (
            current_review.title.title != title_name
            or current_review.title.category != category
        ):

            title, created = Title.objects.get_or_create(
                title=title_name,
                defaults={
                    'category': category,
                    'slug': self.generate_slug(title_name),
                    'pub_year': 2000,
                    'description': '',
                }
            )

            if not created and title.category != category:
                title.category = category
                title.save()

            form.instance.title = title

        messages.success(self.request, 'Отзыв успешно обновлён!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать отзыв'
        context['button_text'] = 'Сохранить изменения'
        return context


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    """Удаление отзыва"""
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('reviews:my_reviews')

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Отзыв успешно удалён!')
        return super().delete(request, *args, **kwargs)
