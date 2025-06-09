
app_name="admin_portal"


from . import views
from django.urls import path
from .views import *

app_name = "admin_portal"

urlpatterns = [
    path("login/",admin_login, name="admin_login"),
    path('',views.dashboard,name='dashboard'),
    path('addmovies/', views.add_movies, name="add_movies"),
    path('manage/', views.view_edit_movies, name='manage_movies'),
    path('edit_movie/<int:id>/',views.edit_movie,name='edit_movie'),
    path('delete_movie/<int:id>/',views.delete_movie,name='delete_movie'),
    path('manage_reviews/',views.view_reviews,name='view_reviews'),
    path('delete_review/<int:id>/',views.delete_review,name='delete_review'),
    path('manage_users/',views.manage_users,name='manage_users'),
    path('block_user/<int:id>/',views.block_user,name='block_user'),
    path('unblock_user/<int:id>/',views.unblock_user,name='unblock_user'),
    path('view_feedbacks/',views.view_feedbacks,name='view_feedbacks'),
    path('view_movie/<int:id>',views.view_movie_details,name = "view_movie"),
    path('admin_logout/',views.admin_logout,name='admin_logout')
]