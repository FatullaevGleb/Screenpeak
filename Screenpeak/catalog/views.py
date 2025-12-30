from django.views.generic import ListView
from .models import Title


class TitleListView(ListView):
    model = Title
    template_name = 'catalog/title_list.html'
    paginate_by = 10
    context_object_name = 'titles'

    def get_queryset(self):
        category = self.kwargs.get('category', 'film')
        return Title.objects.filter(category=category).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('category')
        return context
