from django.contrib import admin
from .models import RoomType, Room, Visitor, Booking, Payment

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_day', 'capacity']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'is_available']
    list_filter = ['room_type', 'is_available']
    search_fields = ['room_number']

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'aadhar_number', 'phone_number', 'age']
    search_fields = ['user__first_name', 'user__last_name', 'aadhar_number', 'phone_number']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Name'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'room', 'check_in_date', 'check_out_date', 'status', 'total_amount']
    list_filter = ['status', 'check_in_date']
    search_fields = ['visitor__user__first_name', 'visitor__user__last_name', 'room__room_number']
    date_hierarchy = 'check_in_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'status', 'payment_date']
    list_filter = ['status', 'payment_date']
    search_fields = ['booking__visitor__user__first_name', 'booking__visitor__user__last_name', 'transaction_id']