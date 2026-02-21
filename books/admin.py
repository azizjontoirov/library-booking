from django.contrib import admin
from .models import Book, Category, Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'total_copies', 'available_copies']
    search_fields = ['title', 'author']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'due_date', 'is_overdue']
    list_filter = ['status']
# Register your models here.
