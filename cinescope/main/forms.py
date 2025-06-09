from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# Movie add form
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = (
            'name', 'director', 'cast', 'release_date', 'description', 'rating', 'image', 
            'genre', 'gross_collection', 'production', 'trailer_id', 'streaming_on', 
            'runtime', 'budget', 'language'
        )

# Review form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("comment", "rating")


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('email','feedback')
    
class WatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = ('user','movie')