from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails
from django.contrib import messages

# Create your views here.
def print_hello(request):
    return HttpResponse("Hello, world!")

def home_page(request):
    return render(request, "Loginify/index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email is unique
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return redirect('signup')

        # Create a new user
        UserDetails.objects.create(username=username, email=email, password=password)
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')

    return render(request, 'Loginify/signup.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists
        try:
            user = UserDetails.objects.get(email=email, password=password)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('confirmation')  # Redirect to a confirmation page
        except UserDetails.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'Loginify/login.html')

def confirmation(request):
    return render(request, 'Loginify/confirmation.html')