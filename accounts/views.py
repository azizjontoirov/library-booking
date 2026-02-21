from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from books.models import Booking

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Xush kelibsiz!')
            return redirect('home')
        else:
            messages.error(request, 'Login yoki parol xato!')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    active = bookings.exclude(status='returned').exclude(status='cancelled').count()
    overdue = [b for b in bookings if b.is_overdue]
    return render(request, 'accounts/profile.html', {
        'bookings': bookings,
        'active': active,
        'overdue': overdue,
    })
