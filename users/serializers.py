from rest_framework import serializers
from .models import User, Event, Booking

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            role=User.USER
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'price', 'category', 'date', 'time', 'location', 'payment_options','available_tickets']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'number_of_tickets', 'is_paid', 'payment_method', 'payment_amount', 'is_confirmed', 'is_cancelled']
        read_only_fields = ['user', 'created_at']