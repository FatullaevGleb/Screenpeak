from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Главная страница"""
    template_name = 'pages/homepage.html'

    def dispatch(self, request, *args, **kwargs):
        """Если пользователь авторизован - редирект на страницу фильмов"""
        if request.user.is_authenticated:
            return redirect('catalog:films')
        return super().dispatch(request, *args, **kwargs)
