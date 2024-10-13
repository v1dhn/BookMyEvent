# API Documentation
 
This document provides an overview of the available APIs for the event management application.
 
## 1. User Registration
- **Endpoint**: `POST /api/register/`
- **Description**: Registers a new user.
- **Request Payload**:
    ```json
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "name": "string"
    }
    ```
- **Responses**:
    - **201 Created**:
      ```json
      {
          "message": "User created successfully"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
          "username": ["This field must be unique."],
          "email": ["Enter a valid email address."]
      }
      ```
      **Reason**: This error may occur if the username is already taken or the email format is incorrect.
 
## 2. User Login
- **Endpoint**: `POST /api/login/`
- **Description**: Logs in a user and provides a JWT token.
- **Request Payload**:
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
- **Responses**:
    - **200 OK**:
      ```json
      {
          "access": "string",
          "refresh": "string"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
          "detail": "No active account found with the given credentials"
      }
      ```
      **Reason**: This error may occur if the username or password is incorrect.
 
## 3. User Logout
- **Endpoint**: `POST /api/logout/`
- **Description**: Logs out a user by blacklisting the refresh token.
- **Request Payload**:
    ```json
    {
        "refresh": "string"
    }
    ```
- **Responses**:
    - **200 OK**:
      ```json
      {
          "message": "Logout successful."
      }
      ```
    - **400 Bad Request**:
      ```json
      {
          "error": "Invalid token"
      }
      ```
      **Reason**: This error may occur if the refresh token is expired or malformed.
 
## 4. Manage User Role
- **Endpoint**: `POST /api/manage-role/`
- **Description**: Admin can promote or demote a user.
- **Request Payload**:
    ```json
    {
        "username":"string",
        "action": "promote" // or "demote"
    }
    ```
- **Responses**:
    - **200 OK**:
      ```json
      {
          "message": "User promoted to Event Manager successfully."
      }
      ```
    - **404 Not Found**:
      ```json
      {
          "error": "User not found."
      }
      ```
      **Reason**: This error occurs if the user ID provided does not exist.
    - **403 Forbidden**:
      ```json
      {
          "detail": "You do not have permission to perform this action."
      }
      ```
      **Reason**: This error occurs if you are not an admin user.
 
## 5. Event List and Details
- **Endpoint**: `GET /api/events/`
- **Description**: Retrieves a list of events or details of a single event.
- **Query Parameters**:
    - `location`: Filter by location (optional, predefined choices: bengaluru/chennai/pune/delhi/mumbai/hyderabad/kolkata/jaipur).
    - `date`: Filter by date (optional).
    - `category`: Filter by category (optional, predefined choices: music/sports/theatre/dance/festival).
- **Example URL**:
    ```
    /api/events/?location=bengaluru&date=2024-10-10&category=music
    ```
- **Responses**:
    - **200 OK**:
      ```json
      [
          {
              "id": 1,
              "title": "string",
              "description": "string",
              "price": "string",
              "category": "string",
              "date": "YYYY-MM-DD",
              "time": "HH:MM:SS",
              "location": "string",
              "payment_options": "string",
              "available_tickets": 100
          }
      ]
      ```
 
## 6. Create Event
- **Endpoint**: `POST /api/events/`
- **Description**: Allows Event Managers to create an event.
- **Request Payload**:
    ```json
    {
        "title": "string",
        "description": "string",
        "price": 300,
        "category": "string", // predefined choices: music/sports/theatre/dance/festival
        "date": "YYYY-MM-DD",
        "time": "HH:MM:SS",
        "location": "string", // predefined choices: bengaluru/chennai/pune/delhi/mumbai/hyderabad/kolkata/jaipur
        "payment_options": "string",
        "available_tickets": 100
    }
    ```
- **Responses**:
    - **201 Created**:
      ```json
      {
          "message": "Event created successfully."
      }
      ```
    - **403 Forbidden**:
      ```json
      {
          "error": "You do not have permission to create events."
      }
      ```
      **Reason**: This error occurs if the authenticated user is not an Event Manager.
 
## 7. Update Event
- **Endpoint**: `PUT /api/events/<int:event_id>/`
- **Description**: Allows Event Managers to update an event. For category, use predefined choices: music/sports/theatre/dance/festival. For location, use predefined choices: bengaluru/chennai/pune/delhi/mumbai/hyderabad/kolkata/jaipur.
- **Request Payload**:
    ```json
    {
        "title": "string",
        "description": "string",
        "price": 300,
        "category": "string", // predefined choices: music/sports/theatre/dance/festival
        "date": "YYYY-MM-DD",
        "time": "HH:MM:SS",
        "location": "string", // predefined choices: bengaluru/chennai/pune/delhi/mumbai/hyderabad/kolkata/jaipur
        "payment_options": "string",
        "available_tickets": 100
    }
    ```
- **Responses**:
    - **200 OK**:
      ```json
      {
          "message": "Event updated successfully."
      }
      ```
    - **403 Forbidden**:
      ```json
      {
          "error": "You do not have permission to edit this event."
      }
      ```
      **Reason**: This error occurs if the authenticated user is not the creator of the event or does not have sufficient permissions.
 
## 8. Partial Update Event (PATCH)
- **Endpoint**: `PATCH /api/events/<int:event_id>/`
- **Description**: Allows Event Managers to partially update an event.
- **Request Payload** (example for partial update):
    ```json
    {
        "available_tickets": 50
    }
    ```
- **Responses**:
    - **200 OK**:
      ```json
      {
          "message": "Event updated successfully."
      }
      ```
    - **403 Forbidden**:
      ```json
      {
          "error": "You do not have permission to edit this event."
      }
      ```
      **Reason**: This error occurs if the authenticated user is not the creator of the event or does not have sufficient permissions.
 
## 9. Book Ticket
- **Endpoint**: `POST /api/book-ticket/`
- **Description**: Allows authenticated users to book tickets for an event.
- **Request Payload**:
    ```json
    {
        "event_id": 1,
        "number_of_tickets": 2
    }
    ```
- **Responses**:
    - **201 Created**:
      ```json
      {
          "message": "Tickets booked successfully.",
          "booking_id": 1
      }
      ```
    - **400 Bad Request**:
      ```json
      {
          "error": "Not enough tickets available."
      }
      ```
      **Reason**: This error occurs if the requested number of tickets exceeds the available tickets for the event.
 
## 10. View User Bookings
- **Endpoint**: `GET /api/my-bookings/`
- **Description**: Retrieves bookings made by the authenticated user.
- **Responses**:
    - **200 OK**:
      ```json
      [
          {
              "id": 1,
              "user": "string",
              "event": "string",
              "number_of_tickets": 2,
              "is_paid": false,
              "payment_method": null,
              "payment_amount": null,
              "is_confirmed": false,
              "is_cancelled": true
          }
      ]
      ```
 
## 11. Cancel Booking
- **Endpoint**: `POST /api/cancel-booking/`
- **Description**: Allows users to cancel their bookings.
- **Request Payload**:
    ```json
    {
        "booking_id": 1
    }
    ```
- **Responses**:
    - **204 No Content**:
      ```json
      {
          "message": "Booking canceled successfully."
      }
      ```
    - **403 Forbidden**:
      ```json
      {
          "error": "You are not authorized to cancel this booking."
      }
      ```
      **Reason**: This error occurs if the booking ID does not belong to the authenticated user.
 
## 12. Make Payment
- **Endpoint**: `POST /api/make-payment/`
- **Description**: Allows users to make payments for their bookings.
- **Request Payload**:
    ```json
    {
        "booking_id": 1,
        "payment_method": "string", // e.g., "credit_card", "debit_card", "paypal"
        "amount": 600
    }
    ```
- **Responses**:
    - **200 OK**:
      ```json
      {
          "message": "Payment successful."
      }
      ```
    - **400 Bad Request**:
      ```json
      {
          "error": "Invalid booking ID or payment amount."
      }
      ```
      **Reason**: This error may occur if the booking ID is incorrect or the amount does not match the ticket price.
 
## 13. Revert Payment
- **Endpoint**: `POST /api/revert-payment/`
- **Description**: Allows users to revert their payments for bookings.
- **Request Payload**:
    ```json
    {
        "booking_id": 1,
        "reason": "string"
    }
    ```
- **Responses**:
    - **200 OK**:
      ```json
      {
          "message": "Payment reverted successfully."
      }
      ```
    - **400 Bad Request**:
      ```json
      {
          "error": "Invalid booking ID."
      }
      ```
      **Reason**: This error may occur if the booking ID does not exist.
 
## 14. Retrieve Event Bookings
- **Endpoint**: `GET /api/event-bookings/<int:event_id>/`
- **Description**: Allows Event Managers to view all bookings for a specific event.
- **Responses**:
    - **200 OK**:
      ```json
      [
          {
              "booking_id": 1,
              "user": "string",
              "number_of_tickets": 2,
              "is_paid": true,
              "payment_method": "credit_card",
              "payment_amount": 600,
              "is_confirmed": true,
              "is_cancelled": false
          }
      ]
      ```
    - **404 Not Found**:
      ```json
      {
          "error": "Event not found."
      }
      ```
      **Reason**: This error occurs if the specified event ID does not exist.
 
## 15. View Event Details
- **Endpoint**: `GET /api/events/<int:event_id>/`
- **Description**: Retrieves detailed information about a specific event.
- **Responses**:
    - **200 OK**:
      ```json
      {
          "id": 1,
          "title": "string",
          "description": "string",
          "price": "string",
          "category": "string",
          "date": "YYYY-MM-DD",
          "time": "HH:MM:SS",
          "location": "string",
          "payment_options": "string",
          "available_tickets": 100
      }
      ```
    - **404 Not Found**:
      ```json
      {
          "error": "Event not found."
      }
      ```
      **Reason**: This error occurs if the specified event ID does not exist.
 