from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from accounts.models import *
from django.db.models.functions import ExtractYear
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .forms import *
def home(request):
    query = request.GET.get('title', '')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    edit_mode = request.GET.get('edit', 'false') == 'true'  # Check if edit mode is enabled

    # Fetch all movies
    movies = Movie.objects.all()

    # Apply search filter
    if query:
        movies = movies.filter(name__icontains=query)

    # Apply year filter
    if start_year and end_year:
        movies = movies.annotate(year=ExtractYear('release_date')).filter(year__range=(start_year, end_year))

    # Fetch movies for "What's New" section
    featured_movies = Movie.objects.order_by('-rating')[:5]
    recent_movies = Movie.objects.order_by('-release_date')[:5]

    context = {
        'movies': movies,
        'featured_movies': featured_movies,
        'recent_movies': recent_movies,
        'search_query': bool(query)
    }
    return render(request, 'main/index.html', context)



def details(request, id):
    movie = get_object_or_404(Movie, id=id)

    # Retrieve reviews for the specific movie
    reviews = Review.objects.filter(movie=movie).order_by("-comment")  # Assuming created_at exists

    is_in_watchlist = None
    # Check if movie is in user's watchlist
    if request.user.is_authenticated:
        is_in_watchlist = WatchList.objects.filter(user=request.user, movie=movie).exists()

    # Calculate average rating
    average = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    if average is None:
        average = None  # Ensuring consistency

    return render(request, 'main/details.html', {
        'movie': movie,
        'reviews': reviews,
        'is_in_watchlist': is_in_watchlist,
        'average': average
    })


def add_movies(request):
    if request.user.is_authenticated:
        # Only allow superusers to add movies
        if request.user.is_superuser:
            if request.method == "POST":
                form = MovieForm(request.POST, request.FILES)  # ✅ Include request.FILES
                if form.is_valid():
                    form.save()
                    return redirect("main:home")
            else:
                form = MovieForm()
            return render(request, 'main/addmovies.html', {"form": form})
        else:
            return redirect("main:home")
    else:
        return redirect("accounts:login")

#manage movies 
def manage_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'main/manage_movies.html')

#review
def add_review(request, id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=id)
        user_review = Review.objects.filter(movie=movie, user=request.user).first()

        if user_review:
            # User has already submitted a review, show a message
            return render(request, 'main/details.html', {"movie": movie, "reviewed": True})

        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("main:details", id=id)
        else:
            form = ReviewForm()

        return render(request, 'main/details.html', {"movie": movie, "form": form})

    else:
        return redirect("accounts:login")
 
def movies_by_year(request, start, end):
    movies = Movie.objects.annotate(year=ExtractYear('release_date')).filter(year__range=(start, end))
    return render(request, 'movies_list.html', {'movies': movies})

def view_edit_movies(request):
    if request.user.is_superuser:
        movies = Movie.objects.all()
        query = request.GET.get('title', '')
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')
        edit_mode = request.GET.get('edit', 'false') == 'true'  # Check if edit mode is enabled

        # Fetch all movies
        movies = Movie.objects.all()

        # Apply search filter
        if query:
            movies = movies.filter(name__icontains=query)

        # Apply year filter
        if start_year and end_year:
            movies = movies.annotate(year=ExtractYear('release_date')).filter(year__range=(start_year, end_year))

        # Fetch movies for "What's New" section
        featured_movies = Movie.objects.order_by('-rating')[:5]
        recent_movies = Movie.objects.order_by('-release_date')[:5]
        context = {
            'movies': movies,
            'featured_movies': featured_movies,
            'recent_movies': recent_movies,
            'search_query': bool(query)
        }
        return render(request, 'main/manage_movies.html', context)


def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie updated successfully!")
            return redirect("main:manage_movies")
    else:
        form = MovieForm(instance=movie)

    return render(request, 'main/edit_movie.html', {'form': form, 'movie': movie})


def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        movie.delete()
        messages.success(request, "Movie deleted successfully!")
        return redirect("main:manage_movies")

    return redirect("main:manage_movies") 


def view_reviews(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:  
            reviews = Review.objects.all()
            return render(request, 'main/manage_reviews.html', {'reviews': reviews})
        else:
            return redirect('home') 
        return redirect('login')  

def delete_review(request,id):
    review = get_object_or_404(Review,id=id)

    if request.method== 'POST':
        review.delete()
        messages.success(request,'Review Deleted Successfully')
        return redirect('main:user_reviews',id = review.user_id)
    
    return redirect('main:user_reviews',id=review.user_id)

def manage_users(request):
    users = CustomUser.objects.all()
    return render(request,'main/manage_users.html',{'users':users})


def user_reviews(request,id):
    if request.user.is_authenticated:
        reviews = Review.objects.filter(user_id = id)
        return render(request,'main/user_reviews.html',{'reviews':reviews})
    else:
        return redirect('login')
    
        
def save_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            
            feedback.save()
            return redirect('main:home')
    else:
        form = FeedbackForm()
    
    return render(request,'main/feedback.html',{'form':form})




def toggle_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    watchlist_item = WatchList.objects.filter(user=request.user, movie=movie)

    if watchlist_item.exists():
        watchlist_item.delete()
    else:
        WatchList.objects.create(user=request.user, movie=movie)  
    return redirect('main:details', id=movie.id)
        

def watchlisted_movie(request):
    if not request.user.is_authenticated:
        return redirect('main:home')
    watchlisted_movies = WatchList.objects.filter(user = request.user).select_related('movie')
    movies = [watchlist.movie for watchlist in watchlisted_movies]

    return render(request,'main/watchlist.html',{'movies':movies})