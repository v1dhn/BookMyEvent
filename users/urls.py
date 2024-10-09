from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ManageUserRoleView, EventView, BookTicketView, BookingListView, CancelBookingView, MakePaymentView, CancelPaymentView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('manage-role/<int:user_id>/', ManageUserRoleView.as_view(), name='manage-role'),
    path('events/', EventView.as_view(), name='create-event'),
    path('events/<int:event_id>/', EventView.as_view(), name='mod-event'),
    path('book-ticket/', BookTicketView.as_view(), name='book-ticket'),
    path('my-bookings/', BookingListView.as_view(), name='my-bookings'),
    path('cancel-booking/<int:booking_id>/', CancelBookingView.as_view(), name='cancel-booking'),
    path('make-payment/', MakePaymentView.as_view(), name='make-payment'),
    path('cancel-payment/', CancelPaymentView.as_view(), name='cancel-payment'),
]
