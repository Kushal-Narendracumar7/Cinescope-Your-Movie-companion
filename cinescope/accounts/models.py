from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib import admin
from main.models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name", "director", "release_date", "rating", "runtime", "language", "streaming_on")
    search_fields = ("name", "director", "cast", "genre")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "rating", "comment")
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    mobile_no = models.CharField(max_length=15, unique=True,null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    favorite_genre = models.CharField(max_length=50, choices=[
        ('Action', 'Action'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Horror', 'Horror'),
        ('Sci-Fi', 'Sci-Fi'), ('Romance', 'Romance')
    ], blank=True, null=True)
    is_admin = models.BooleanField(default=False)  # ✅ For custom admin role

    def __str__(self):
        return self.username
