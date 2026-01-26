from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from apps.concerns.utils import generate_random_alias

def register_view(request):
    if request.user.is_authenticated:
        return redirect('concerns:list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Generate random alias if not provided (though form doesn't have alias field yet)
            # But the user model has it.
            user.alias = generate_random_alias()
            user.save()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('concerns:list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'security_management/pages/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('concerns:list')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'concerns:list'))
    else:
        form = UserLoginForm()
    
    return render(request, 'security_management/pages/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # If alias is cleared, regenerate it? Or allow blank?
            # User wants: "set random display names... but also allow them to set their own"
            # If they clear it, maybe regenerate?
            user = form.save(commit=False)
            if not user.alias:
                user.alias = generate_random_alias()
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('security_management:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'security_management/pages/profile.html', {'form': form})