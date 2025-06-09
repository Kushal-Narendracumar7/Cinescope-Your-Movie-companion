from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models.functions import ExtractYear
from requests import session
from accounts.models import CustomUser
from main.forms import MovieForm
from main.models import Feedback, Movie,Review
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
User = get_user_model() 

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active and getattr(user, "is_admin", False):  
                login(request, user)
                return redirect("admin_portal:dashboard")
            else:
                messages.error(request, "Your account is not active or lacks admin access.")
        else:
            messages.error(request, "Invalid username or password.")
        
        return redirect("admin_portal:admin_login")

    return render(request, 'admin_portal/login.html')




@login_required(login_url='admin_portal:admin_login')
def dashboard(request):
    if request.user.is_authenticated:
        if getattr(request.user, "is_admin", False): 
            users_count = CustomUser.objects.count()
            movies_count = Movie.objects.count()
            reviews_count = Review.objects.count()
            feedback_counts = Feedback.objects.count()
            recent_actions = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:5]
       
            return render(request, 'admin_portal/dashboard.html', {
                'users': users_count,
                'movies': movies_count,
                'reviews': reviews_count,
                'recent_actions': recent_actions,
                'feedbacks':feedback_counts
        })
    
        messages.error(request, "You do not have admin privileges.")
        return redirect("admin_portal:admin_login")


def add_movies(request):
    if request.user.is_authenticated:
        # Only allow superusers to add movies
        if request.user.is_admin:
            if request.method == "POST":
                form = MovieForm(request.POST, request.FILES)  # ✅ Include request.FILES
                if form.is_valid():
                    movie = form.save()
                    log_admin_action(request.user, movie, ADDITION, f"Added movie: {movie}")
                    return redirect("admin_portal:dashboard")
            else:
                form = MovieForm()
            return render(request, 'admin_portal/addmovies.html', {"form": form})
        else:
            return redirect("admin_portal:dashboard")
    else:
        return redirect("admin_portal:admin_login")

def manage_movies(request):
    if request.user.is_authenticated:
        if request.user.is_admin==True:
            return render(request,'admin_portal/manage_movies.html')

@login_required
def view_edit_movies(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("You do not have permission to access this page.")

    movies = Movie.objects.all()
    query = request.GET.get('title', '')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    edit_mode = request.GET.get('edit', 'false') == 'true'  # Check if edit mode is enabled

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
        'search_query': bool(query),
    }
    return render(request, 'admin_portal/manage_movies.html', context)


def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            log_admin_action(request.user,movie,CHANGE,f"Edited Movie:{movie}")
            messages.success(request, "Movie updated successfully!")
            return redirect("admin_portal:manage_movies")
    else:
        form = MovieForm(instance=movie)

    return render(request, 'admin_portal/edit_movie.html', {'form': form, 'movie': movie})


def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        log_admin_action(request.user,movie,DELETION,f"Deleted Movie:{movie}")
        movie.delete()

        messages.success(request, "Movie deleted successfully!")
        return redirect("admin_portal:manage_movies")

    return redirect("admin_portal:manage_movies") 

def delete_review(request,id):
    review = get_object_or_404(Review,id=id)

    if request.method== 'POST':
        log_admin_action(request.user, review, DELETION, f"Deleted review: {review}")
        review.delete()
        messages.success(request,'Review Deleted Successfully')
        return redirect('admin_portal:view_reviews')
    
    return redirect('admin_portal:view_reviews')

def view_movie_details(request, id):
    movie = get_object_or_404(Movie, id=id)

    # Retrieve reviews for the specific movie
    reviews = Review.objects.filter(movie=movie).order_by("-comment")  # Assuming created_at exists

    

    # Calculate average rating
    average = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    if average is None:
        average = None 

    return render(request, 'admin_portal/view_movie.html', {
        'movie': movie,
        'reviews': reviews,
        'average': average
    })

def view_reviews(request):
    if request.user.is_authenticated:
        if request.user.is_admin:  
            reviews = Review.objects.all()
            return render(request, 'admin_portal/manage_reviews.html', {'reviews': reviews})
        else:
            return redirect('admin_portal:dashboard')  
    return redirect('admin_portal:admin_login')  # Redirect unauthenticated users to login



def manage_users(request):
    users = CustomUser.objects.all()
    return render(request,'admin_portal/manage_users.html',{'users':users})


def block_user(request,id):
    user = get_object_or_404(CustomUser,id=id)
    if request.method == 'POST':
        if user.is_active == False:
            messages.success(request,'User already blocked')
            return redirect('admin_portal:manage_users')
        user.is_active = False
        user.save()
        log_admin_action(request.user, user, CHANGE, f"Blocked user: {user}")
        messages.success(request,'User got Blocked')
        return redirect('admin_portal:manage_users')
    return redirect('admin_portal:manage_users')


def unblock_user(request,id):
    user = get_object_or_404(CustomUser,id=id)
    if request.method == 'POST':
        user.is_active = True
        user.save()
        log_admin_action(request.user, user, CHANGE, f"Unblocked user: {user}")
        messages.success(request,'User got Unblocked')
        return redirect('admin_portal:manage_users')
    return redirect('admin_portal:manage_users')

def log_admin_action(user, obj, action_flag, message):
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(obj).id,
        object_id=obj.id,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=message
    )

def view_feedbacks(request):
    if request.user.is_admin:
        feedbacks = Feedback.objects.all()
        return render(request,'admin_portal/view_feedbacks.html',{'feedbacks':feedbacks})
    else:
        return redirect('admin_portal:dashboard')  
    

def admin_logout(request):
    if request.user.is_authenticated and getattr(request.user, 'is_admin', False):
        logout(request)
    return redirect('admin_portal:admin_login')