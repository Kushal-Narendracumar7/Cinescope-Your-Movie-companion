
app_name="accounts"
from django.contrib.auth.views import PasswordChangeDoneView,PasswordChangeView

from django.urls import path, reverse_lazy
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
   path('password_change/', PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url=reverse_lazy('accounts:password_change_done')  
    ), name='password_change'),
    
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
