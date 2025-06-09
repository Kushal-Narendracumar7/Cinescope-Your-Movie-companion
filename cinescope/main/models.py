from django.db import models
from django.conf import settings  # Reference for custom user model

class Movie(models.Model):
    name = models.CharField(max_length=300)
    director = models.CharField(max_length=300)
    cast = models.CharField(max_length=300)
    release_date = models.DateField()
    description = models.TextField(max_length=5000)
    rating = models.FloatField(default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    genre = models.CharField(max_length=300, null=True, blank=True)  
    gross_collection = models.BigIntegerField(null=True, blank=True)  
    production = models.CharField(max_length=300, null=True, blank=True)  
    trailer_id = models.CharField(max_length=300, null=True, blank=True)  
    streaming_on = models.CharField(max_length=300, null=True, blank=True)  
    runtime = models.PositiveIntegerField(null=True, blank=True)  
    budget = models.BigIntegerField(null=True, blank=True)  
    language = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True, max_length=1000)
    rating = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        """Ensure rating is between 0 and 10"""
        if self.rating < 0:
            self.rating = 0
        elif self.rating > 10:
            self.rating = 10
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True) 
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else self.email or 'Anonymous'}"

class WatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    watched = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.user.username}'s WatchList - {self.movie.name}"

