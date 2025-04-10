from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import RoomType, Room, Visitor, Booking, Payment
from .forms import UserRegistrationForm, VisitorForm, BookingForm, RoomSearchForm
from datetime import datetime, timedelta

def home(request):
    room_types = RoomType.objects.all()[:3]  # Get a few room types to display on home page
    
    # Handle room search form
    form = RoomSearchForm(request.GET or None)
    available_rooms = []
    
    if form.is_valid():
        check_in_date = form.cleaned_data['check_in_date']
        check_out_date = form.cleaned_data['check_out_date']
        adults = form.cleaned_data['adults']
        
        # Find rooms that are available for the selected dates
        booked_rooms = Booking.objects.filter(
            Q(check_in_date__lte=check_out_date) & 
            Q(check_out_date__gte=check_in_date) &
            Q(status__in=['pending', 'confirmed'])
        ).values_list('room__id', flat=True)
        
        available_rooms = Room.objects.exclude(id__in=booked_rooms)
        
        # Filter by capacity
        available_rooms = available_rooms.filter(room_type__capacity__gte=adults)
        
        # Store search parameters in session for booking process
        request.session['search_data'] = {
            'check_in_date': check_in_date.isoformat(),
            'check_out_date': check_out_date.isoformat(),
            'adults': adults,
            'children': form.cleaned_data.get('children', 0)
        }
    
    context = {
        'room_types': room_types,
        'form': form,
        'available_rooms': available_rooms
    }
    return render(request, 'booking/home.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        visitor_form = VisitorForm(request.POST)
        
        if user_form.is_valid() and visitor_form.is_valid():
            user = user_form.save()
            visitor = visitor_form.save(commit=False)
            visitor.user = user
            visitor.save()
            
            login(request, user)
            messages.success(request, 'Registration successful! You can now book rooms.')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        visitor_form = VisitorForm()
    
    return render(request, 'booking/register.html', {
        'user_form': user_form,
        'visitor_form': visitor_form
    })

@login_required
def room_list(request):
    # Get search data from session if available
    search_data = request.session.get('search_data', None)
    
    if not search_data:
        messages.warning(request, 'Please search for availability first.')
        return redirect('home')
    
    check_in_date = datetime.fromisoformat(search_data['check_in_date']).date()
    check_out_date = datetime.fromisoformat(search_data['check_out_date']).date()
    adults = search_data['adults']
    
    # Find booked rooms for the selected dates
    booked_rooms = Booking.objects.filter(
        Q(check_in_date__lte=check_out_date) & 
        Q(check_out_date__gte=check_in_date) &
        Q(status__in=['pending', 'confirmed'])
    ).values_list('room__id', flat=True)
    
    # Get available rooms
    available_rooms = Room.objects.exclude(id__in=booked_rooms)
    
    # Group by room type
    room_types = RoomType.objects.filter(rooms__in=available_rooms).distinct()
    
    # Calculate stay duration
    days = (check_out_date - check_in_date).days
    
    context = {
        'room_types': room_types,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'days': days,
        'adults': adults,
        'children': search_data.get('children', 0)
    }
    return render(request, 'booking/room_list.html', context)

@login_required
def book_room(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    search_data = request.session.get('search_data', None)
    
    if not search_data:
        messages.warning(request, 'Please search for availability first.')
        return redirect('home')
    
    check_in_date = datetime.fromisoformat(search_data['check_in_date']).date()
    check_out_date = datetime.fromisoformat(search_data['check_out_date']).date()
    adults = search_data['adults']
    children = search_data.get('children', 0)
    
    # Find available room of this type
    booked_rooms = Booking.objects.filter(
        Q(check_in_date__lte=check_out_date) & 
        Q(check_out_date__gte=check_in_date) &
        Q(status__in=['pending', 'confirmed'])
    ).values_list('room__id', flat=True)
    
    available_room = Room.objects.filter(room_type=room_type).exclude(id__in=booked_rooms).first()
    
    if not available_room:
        messages.error(request, 'Sorry, this room type is no longer available for the selected dates.')
        return redirect('room_list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            try:
                visitor = request.user.visitor
            except Visitor.DoesNotExist:
                messages.error(request, 'Your profile is incomplete. Please update your details.')
                return redirect('update_profile')
            
            booking.visitor = visitor
            booking.room = available_room
            booking.check_in_date = check_in_date
            booking.check_out_date = check_out_date
            booking.adults = adults
            booking.children = children
            
            # Calculate total amount
            days = (check_out_date - check_in_date).days
            booking.total_amount = room_type.price_per_day * days
            
            booking.save()
            
            # Create a pending payment
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.total_amount,
                status='pending'
            )
            
            messages.success(request, 'Your booking is confirmed!')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        initial_data = {
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'adults': adults,
            'children': children
        }
        form = BookingForm(initial=initial_data)
    
    # Calculate total amount
    days = (check_out_date - check_in_date).days
    total_amount = room_type.price_per_day * days
    
    context = {
        'form': form,
        'room_type': room_type,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'days': days,
        'total_amount': total_amount,
        'adults': adults,
        'children': children
    }
    return render(request, 'booking/booking_form.html', context)

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, visitor__user=request.user)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})

@login_required
def user_bookings(request):
    try:
        visitor = request.user.visitor
        bookings = Booking.objects.filter(visitor=visitor).order_by('-booking_date')
    except Visitor.DoesNotExist:
        bookings = []
    
    return render(request, 'booking/user_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, visitor__user=request.user)
    
    # Only allow cancellation of pending or confirmed bookings
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        
        # Update payment status if exists
        if hasattr(booking, 'payment'):
            booking.payment.status = 'refunded'
            booking.payment.save()
        
        messages.success(request, 'Your booking has been cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('user_bookings')

@login_required
def update_profile(request):
    try:
        visitor = request.user.visitor
    except Visitor.DoesNotExist:
        visitor = None
    
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.user = request.user
            visitor.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_bookings')
    else:
        form = VisitorForm(instance=visitor)
    
    return render(request, 'booking/update_profile.html', {'form': form})