"""
URL configuration for moviereview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
app_name="main"

from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.details, name="details"),
    path('addreview/<int:id>', views.add_review, name='add_review'),
    path('movies/year/<int:start>/<int:end>/', views.movies_by_year, name='movies_by_year'),
    path('user_reviews/<int:id>/',views.user_reviews,name='user_reviews'),
    path('delete_review/<int:id>/',views.delete_review,name='delete_review'),
    path('feedback/',views.save_feedback,name='feedback'),
    path('watchlist/',views.watchlisted_movie,name='watchlist'),
    path('toggle_watchlist/<int:movie_id>/', views.toggle_watchlist, name='toggle_watchlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)