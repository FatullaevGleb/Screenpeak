from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.MyReviewsView.as_view(), name='my_reviews'),
    path('add/', views.AddReviewView.as_view(), name='add'),
    path('<int:pk>/edit/', views.EditReviewView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete'),
]
