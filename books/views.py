from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from .models import Book, Booking, Category

def home(request):
    return render(request, 'home.html')

def book_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    books = Book.objects.all()
    
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)
    if category_id:
        books = books.filter(category_id=category_id)
    
    categories = Category.objects.all()
    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': categories,
        'query': query,
    })

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_booking = Booking.objects.filter(
        user=request.user, book=book
    ).exclude(status='returned').exclude(status='cancelled').first()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'user_booking': user_booking,
    })

@login_required
def book_booking(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if book.available_copies <= 0:
        messages.error(request, 'Bu kitob hozirda mavjud emas!')
        return redirect('book_detail', pk=pk)
    
    existing = Booking.objects.filter(
        user=request.user, book=book
    ).exclude(status='returned').exclude(status='cancelled').first()
    
    if existing:
        messages.warning(request, 'Siz bu kitobni allaqachon band qilgansiz!')
        return redirect('book_detail', pk=pk)
    
    due_date = date.today() + timedelta(days=14)
    Booking.objects.create(
        user=request.user,
        book=book,
        due_date=due_date,
        status='pending'
    )
    book.available_copies -= 1
    book.save()
    
    messages.success(request, f'Kitob muvaffaqiyatli band qilindi! Qaytarish muddati: {due_date}')
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'books/my_bookings.html', {'bookings': bookings})


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def librarian_panel(request):
    bookings = Booking.objects.all().order_by('-booked_at')
    return render(request, 'books/librarian_panel.html', {'bookings': bookings})

@staff_member_required
def update_booking(request, pk, action):
    booking = get_object_or_404(Booking, pk=pk)
    
    if action == 'approve':
        booking.status = 'approved'
        messages.success(request, 'Buyurtma tasdiqlandi!')
    elif action == 'return':
        booking.status = 'returned'
        booking.returned_at = timezone.now()
        booking.book.available_copies += 1
        booking.book.save()
        messages.success(request, 'Kitob qaytarildi!')
    elif action == 'cancel':
        booking.status = 'cancelled'
        booking.book.available_copies += 1
        booking.book.save()
        messages.warning(request, 'Buyurtma bekor qilindi!')
    
    booking.save()
    return redirect('librarian_panel')