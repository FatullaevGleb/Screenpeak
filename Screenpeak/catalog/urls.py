from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('films/', views.TitleListView.as_view(), {'category': 'film'}, name='films'),
    path('series/', views.TitleListView.as_view(), {'category': 'series'}, name='series'),
    path('anime/', views.TitleListView.as_view(), {'category': 'anime'}, name='anime'),
]
