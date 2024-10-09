from django.contrib import admin
from .models import Event, User, Booking

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'available_tickets', 'created_by')
    search_fields = ('title', 'location')
    list_filter = ('date', 'location')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','name','email','role')
    list_filter = ('role',)
    list_display_links = ('username',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'number_of_tickets', 'created_at')
    list_filter = ('user', 'event', 'created_at')