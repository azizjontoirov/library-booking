from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('<int:pk>/booking/', views.book_booking, name='book_booking'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('librarian/', views.librarian_panel, name='librarian_panel'),
    path('librarian/<int:pk>/<str:action>/', views.update_booking, name='update_booking'),
]