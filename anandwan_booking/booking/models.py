from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_types/', null = True, blank = True)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    room_number = models.CharField(max_length = 10)
    room_type = models.ForeignKey(RoomType, on_delete = models.CASCADE, related_name='rooms')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} - {self.room_type.name}"
    

class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    aadhar_number = models.CharField(max_length=12, unique= True)
    phone_number = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    address = models.TextField()   

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', "Pending"),
        ('confirmed', "Confirmed"),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ) 

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name ='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES, default ='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    adults = models.PositiveIntegerField(default =1)
    children = models.PositiveIntegerField(default=0)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.visitor.user.first_name} - {self.room.room_number} - {self.check_in_date}"
    
    def save(self, *args, **kwargs):
        if not self.total_amount:
            days = (self.check_out_date - self.check_in_date).days
            self.total_amount = self.room.room_type.price_per_day * days
        super().save(*args, **kwargs)

    def is_active(self):
        return self.status in ['pending', 'confirmed']
    

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places = 2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices= PAYMENT_STATUS_CHOICES, default ='pending')

    def __str__(self):
        return f"{self.booking.visitor.user.first_name} - {self.amount} - {self.status}"