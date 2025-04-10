from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Visitor, Booking, Room
from datetime import date

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class VisitorForm(forms.ModelForm):
    aadhar_number = forms.CharField(
        max_length=12, 
        min_length=12, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 12-digit Aadhar number'})
    )
    
    class Meta:
        model = Visitor
        fields = ['aadhar_number', 'phone_number', 'age', 'address']
        
    def clean_aadhar_number(self):
        aadhar = self.cleaned_data.get('aadhar_number')
        if not aadhar.isdigit():
            raise forms.ValidationError("Aadhar number must contain only digits")
        return aadhar

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['special_requests']  # Only include special_requests field
        
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Make special_requests optional
        self.fields['special_requests'].required = False

class RoomSearchForm(forms.Form):
    check_in_date = forms.DateField(widget=DateInput())
    check_out_date = forms.DateField(widget=DateInput())
    adults = forms.IntegerField(min_value=1, initial=1)
    children = forms.IntegerField(min_value=0, initial=0, required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        
        if check_in_date and check_out_date:
            # Check if check-in date is not in the past
            if check_in_date < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")
            
            # Check if check-out date is after check-in date
            if check_out_date <= check_in_date:
                raise forms.ValidationError("Check-out date must be after check-in date.")
        
        return cleaned_data