from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    USER = 'user'
    EVENT_MANAGER = 'event_manager'
    
    ROLE_CHOICES = [
        (USER, 'User'),
        (EVENT_MANAGER, 'Event Manager'),
    ]
    
    email = models.EmailField(unique=True, blank=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return self.username


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('theatre', 'Theatre'),
        ('dance', 'Dance'),
    ]

    CITY_CHOICES = [
        ('bengaluru', 'Bengaluru'),
        ('hyderabad', 'Hyderabad'),
        ('chennai', 'Chennai'),
        ('delhi', 'Delhi'),
        ('mumbai', 'Mumbai'),
        ('pune', 'Pune'),
        ('kolkata', 'Kolkata'),
        ('jaipur', 'Jaipur'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=50, choices=CITY_CHOICES)
    payment_options = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    available_tickets = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    number_of_tickets = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    is_cancelled = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} booked {self.number_of_tickets} ticket(s) for {self.event.title}"