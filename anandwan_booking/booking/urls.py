from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rooms/', views.room_list, name='room_list'),
    path('book/<int:room_type_id>/', views.book_room, name='book_room'),
    path('bookings/', views.user_bookings, name='user_bookings'),
    path('booking/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('profile/update/', views.update_profile, name='update_profile'),
]