from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Event, Booking
from .serializers import RegisterSerializer, EventSerializer, BookingSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ManageUserRoleView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            action = request.data.get("action")
            
            if action == "promote":
                user.role = User.EVENT_MANAGER
                user.save()
                return Response({"message": "User promoted to Event Manager successfully."}, status=status.HTTP_200_OK)
            elif action == "demote":
                user.role = User.USER
                user.save()
                return Response({"message": "User demoted to regular User successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action. Use 'promote' or 'demote'."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    

class EventView(APIView):

    # Allow unauthenticated users to view the events too
    permission_classes = [AllowAny]

    def get(self, request, event_id=None):
        """Retrieve a list of events or a single event for all users."""
        if event_id is not None:
            # Retrieve a specific event by ID (if provided)
            event = get_object_or_404(Event, id=event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Otherwise retrieve all events
        events = Event.objects.all()

        location = request.query_params.get('location')
        date = request.query_params.get('date')
        category = request.query_params.get('category')

        if location:
            events = events.filter(location=location)
        if date:
            events = events.filter(date=date)
        if category:
            events = events.filter(category=category)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Helper function to check authentication and event_manager role
    def is_event_manager(self, user):
        return user.is_authenticated and user.role == 'event_manager'

    def post(self, request):
        if not self.is_event_manager(request.user):
            return Response({"error": "You do not have permission to create events."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": "Event created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if not self.is_event_manager(request.user):
            return Response({"error": "You do not have permission to edit this event."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if not self.is_event_manager(request.user):
            return Response({"error": "You do not have permission to edit this event."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if not self.is_event_manager(request.user):
            return Response({"error": "You do not have permission to delete this event."}, status=status.HTTP_403_FORBIDDEN)

        bookings = Booking.objects.filter(event=event)

        for booking in bookings:
            if booking.is_paid:
                booking.is_paid = False
                booking.is_confirmed = False
                booking.payment_method = None
                booking.save()
            booking.is_cancelled = True
            booking.save()

        event.delete()
        return Response({"message": "Event deleted successfully. All associated bookings have been cancelled and refund has been initiated"}, status=status.HTTP_204_NO_CONTENT)
    
class BookTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_id = request.data.get("event_id")
        number_of_tickets = request.data.get("number_of_tickets")

        # If the event exists
        event = get_object_or_404(Event, id=event_id)

        # Checking for enough tickets
        if number_of_tickets > event.available_tickets:
            return Response({"error": "Not enough tickets available."}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = event.price*number_of_tickets
        booking = Booking.objects.create(user=request.user, event=event, number_of_tickets=number_of_tickets, price_per_ticket=event.price,payment_amount=amount)

        # Update available tickets for the event
        event.available_tickets -= number_of_tickets
        event.save()

        return Response({"message": "Tickets booked successfully.", "booking_id": booking.id}, status=status.HTTP_201_CREATED)

class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.user != request.user:
            return Response({"error": "You do not have permission to cancel this booking."}, status=status.HTTP_403_FORBIDDEN)

        event = booking.event

        event.available_tickets += booking.number_of_tickets
        event.save()

        if booking.is_paid:
            booking.is_paid = False
            booking.is_confirmed = False
            booking.payment_method = None
            booking.save()

            # We can add payment refund processing logic here
        
        booking.is_cancelled = True
        booking.save()

        return Response({"message": "Booking canceled successfully. Refund has been initiated"}, status=status.HTTP_204_NO_CONTENT)

class MakePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get("booking_id")
        payment_method = request.data.get("payment_method")

        booking = get_object_or_404(Booking, id=booking_id)

        if booking.user != request.user:
            return Response({"error": "You do not have permission to pay for this booking."}, status=status.HTTP_403_FORBIDDEN)

        if booking.is_paid:
            return Response({"error": "Booking is already paid."}, status=status.HTTP_400_BAD_REQUEST)


        booking.is_paid = True
        booking.payment_method = payment_method
        booking.is_confirmed = True
        booking.save()

        return Response({"message": "Payment successful. Booking confirmed.", "amount_paid": booking.payment_amount}, status=status.HTTP_200_OK)

class CancelPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.user != request.user:
            return Response({"error": "You do not have permission to cancel this payment."}, status=status.HTTP_403_FORBIDDEN)

        if not booking.is_paid:
            return Response({"error": "Payment has not been made."}, status=status.HTTP_400_BAD_REQUEST)

        booking.is_paid = False
        booking.payment_method = None
        booking.is_confirmed = False
        booking.save()

        return Response({"message": "Payment canceled successfully. Refund has been initiated"}, status=status.HTTP_200_OK)
