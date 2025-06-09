from traceback import format_tb
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from accounts.models import CustomUser 
from django.utils.html import format_html

# Customize Movie Admin
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'director', 'release_date', 'rating', 'genre', 'language', 'runtime', 'budget')
    search_fields = ('name', 'director', 'genre', 'language')
    list_filter = ('genre', 'language', 'release_date')

# Customize Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'comment')
    search_fields = ('user__username', 'movie__name')
    list_filter = ('rating',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user','email','feedback')
    search_fields = ('user__username',  )


# ✅ Customize CustomUser Admin (Updated Fields)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'mobile_no', 'gender', 'nationality', 'date_of_birth', 'favorite_genre', 'is_admin', 'display_profile_picture')  
    search_fields = ('username', 'email', 'mobile_no', 'nationality', 'favorite_genre')  
    list_filter = ('gender', 'nationality', 'favorite_genre', 'is_admin')  

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("mobile_no", "profile_picture", "gender", "nationality", "date_of_birth", "favorite_genre", "is_admin")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("mobile_no", "profile_picture", "gender", "nationality", "date_of_birth", "favorite_genre", "is_admin")}),
    )

    # ✅ Display profile picture in admin panel
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.profile_picture.url)
        return "No Image"
    display_profile_picture.short_description = "Profile Picture"

class WatchListAdmin(admin.ModelAdmin):
    model = WatchList
    list_display = ['user','movie','watched']
    search_fields=['user','movie']



# ✅ Registering models safely (avoiding AlreadyRegistered errors)
try:
    admin.site.register(Movie, MovieAdmin)
except admin.sites.AlreadyRegistered:
    pass 

try:
    admin.site.register(Review, ReviewAdmin)
except admin.sites.AlreadyRegistered:
    pass 

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(WatchList,WatchListAdmin)