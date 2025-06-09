from email import message_from_string
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError  # Import IntegrityError
from .forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm  # Import your form
from django.core.mail import send_mail
import random 
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  # Prevent login until email verification
                user.save()

                otp = random.randint(100000, 999999)

                # Store OTP and email in session
                request.session['otp'] = otp
                request.session['email'] = user.email

                # Send OTP email
                send_mail(
                    "Cinescope: Email Verification OTP",
                    f"Hello {user.username},\n\nYour OTP for email verification is: {otp}.\n\nEnter this OTP to activate your account.\n\nThank you!",
                    'noreplyCinescope@gmail.com',
                    [user.email],
                    fail_silently=False
                )

                messages.info(request, "An OTP has been sent to your email. Please verify your account.")
                return redirect('accounts:verify_otp')

            except IntegrityError as e :  
                form.add_error("username", e)

    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})#login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
             if user.is_active:
                login(request, user)
                return redirect("main:home")
             else:
                return render(request, 'accounts/login.html', {'error': "Your Account has been disabled"})

        else:
            return render(request, 'accounts/login.html', {'error': "Invalid Username/Password"})

    return render(request, 'accounts/login.html')


CustomUser = get_user_model() 
#logout user
def logout_user(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def edit_profile(request):
    user = request.user
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:edit_profile")  # Use the correct namespace if applicable

    else:
        form = EditProfileForm(instance=user)

    return render(request, "accounts/edit_profile.html", {"form": form, "user": user})


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        email = request.session.get('email')

        if stored_otp and email and entered_otp:
            if int(entered_otp) == stored_otp:
                user = CustomUser.objects.get(email=email)
                user.is_active = True  # Activate the account
                user.save()

                # Clear session data
                del request.session['otp']
                del request.session['email']

                messages.success(request, "Account verified successfully! You can now log in.")
                return redirect('accounts:login')
            else:
                messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'accounts/verify_otp.html')

