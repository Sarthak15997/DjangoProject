from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
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

def get_all_users(request):
    users = UserDetails.objects.all()
    user_list = [{"username": user.username, "email": user.email, "password": user.password} for user in users]
    return JsonResponse(user_list, safe=False)

def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user_data = {"username":user.username, "email":user.email, "password":user.password}
        return JsonResponse(user_data)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User Not Found"}, status = 404)

def update_user(request, email):
    try:
        # Retrieve the user by email
        user = UserDetails.objects.get(email=email)

        if request.method == 'POST':
            # Update the user fields if provided in the request
            new_username = request.POST.get('username')
            new_email = request.POST.get('email')
            new_password = request.POST.get('password')

            if new_email and new_email != user.email:
                if UserDetails.objects.filter(email=new_email).exists():
                    return JsonResponse({"error": "Email already exists"}, status=400)
                user.email = new_email

            if new_username:
                user.username = new_username
            if new_password:
                user.password = new_password

            # Save the updated user
            user.save()

            return JsonResponse({"message": "User updated successfully"})
        else:
            return JsonResponse({"error": "POST request required"}, status=400)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

def delete_user(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"})
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)