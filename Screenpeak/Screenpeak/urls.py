from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('catalog/', include('catalog.urls')),
    # path('reviews/', include('reviews.urls')),
    # path('auth/', include('django.contrib.auth.urls')),
]
