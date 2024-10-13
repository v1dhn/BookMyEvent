from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Event, Booking

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.manage_role_url = reverse('manage-role')
        self.event_url = reverse('create-event')
        self.booking_url = reverse('book-ticket')
        self.payment_url = reverse('make-payment')
        self.cancel_payment_url = reverse('cancel-payment')

        User.objects.filter(username='testuser').delete()
        User.objects.filter(email='testuser@example.com').delete()

        # User data for registration
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'name': 'Test User',
            'password': 'testpassword'
        }
        # Admin data for testing
        self.admin_data = {
            'username': 'adminuser',
            'email': 'adminuser@example.com',
            'name': 'Admin User',
            'password': 'adminpassword'
        }
        # Create admin user
        self.admin = User.objects.create_superuser(**self.admin_data)

    def test_user_registration(self):
        # Ensure the user can register successfully
        response = self.client.post(self.register_url, self.user_data)
        print(response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        # First, register the user
        self.client.post(self.register_url, self.user_data)
        # Test the login functionality
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_admin_promote_user(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        # Register a user to promote
        user_to_promote = User.objects.create_user(
            username='user_to_promote',
            email='user_to_promote@example.com',
            password='userpassword'
        )
        # Promote the user
        response = self.client.post(self.manage_role_url, {
            'username': user_to_promote.username,
            'action': 'promote'
        })
        user_to_promote.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_to_promote.role, 'event_manager')

    def test_non_admin_cannot_promote(self):
        # Create a non-admin user
        non_admin_user = User.objects.create_user(
            username='regularuser',
            email='regularuser@example.com',
            password='userpassword'
        )
        self.client.force_authenticate(user=non_admin_user)
        response = self.client.post(self.manage_role_url, {
            'username': self.admin.username,
            'action': 'promote'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class EventTests(APITestCase):
    def setUp(self):
        self.event_url = reverse('create-event')
        self.event_manager_data = {
            'username': 'eventmanager',
            'email': 'eventmanager@example.com',
            'name': 'Event Manager',
            'password': 'managerpassword'
        }
        self.event_manager = User.objects.create_user(**self.event_manager_data)
        self.event_manager.role = 'event_manager'
        self.event_manager.save()
        
        self.event_data = {
            'title': 'Music Concert',
            'description': 'A grand music concert.',
            'date': '2024-12-15',
            'time': '18:00:00',
            'location': 'bengaluru',
            'category': 'music',
            'payment_options': 'card, net banking',
            'available_tickets': 100,
            'price': 500.00
        }

    
    def test_create_event(self):
    # Ensure the event manager is authenticated
        self.client.force_authenticate(user=self.event_manager)
        
        response = self.client.post(self.event_url, self.event_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

    def test_non_event_manager_cannot_create_event(self):
        regular_user = User.objects.create_user(
            username='regularuser',
            email='regularuser@example.com',
            password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        response = self.client.post(self.event_url, self.event_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.event_manager = User.objects.create_user(
            username='eventmanager',
            email='eventmanager@example.com',
            password='managerpassword',
            role='event_manager'
        )
        self.event = Event.objects.create(
            title='Music Concert',
            description='A grand music concert.',
            date='2024-12-15',
            time='18:00:00',
            location='bengaluru',
            category='music',
            payment_options='card, net banking',
            available_tickets=100,
            price=500.00,
            created_by=self.event_manager
        )
        self.booking_url = reverse('book-ticket')
        self.access_token = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        }).data['access']

    def test_book_ticket(self):
        booking_data = {
            'event_id': self.event.id,
            'number_of_tickets': 2
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.booking_url, booking_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_booking_not_enough_tickets(self):
        booking_data = {
            'event_id': self.event.id,
            'number_of_tickets': 200  # More than available tickets
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.booking_url, booking_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PaymentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.event_manager = User.objects.create_user(
            username='eventmanager',
            email='eventmanager@example.com',
            password='managerpassword',
            role='event_manager'
        )
        self.event = Event.objects.create(
            title='Music Concert',
            description='A grand music concert.',
            date='2024-12-15',
            time='18:00:00',
            location='bengaluru',
            category='music',
            payment_options='card, net banking',
            available_tickets=100,
            price=500.00,
            created_by=self.event_manager
        )
        self.booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            number_of_tickets=2,
            price_per_ticket=500.00
        )
        self.access_token = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        }).data['access']

    def test_make_payment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(reverse('make-payment'), {
            'booking_id': self.booking.id,
            'payment_method': 'card'
        })
        self.booking.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.booking.is_paid)

    def test_cancel_payment(self):
        self.booking.is_paid = True
        self.booking.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(reverse('cancel-payment'), {
            'booking_id': self.booking.id
        })
        self.booking.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.booking.is_paid)
