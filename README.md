# Face Recognition Security System

## Overview
This project is a Face Recognition Security System built with Django and Django REST Framework. It provides a robust API for user registration, authentication, and emotion detection through facial recognition.

## Features
- User registration and authentication
- Face detection and emotion recognition
- Real-time emotion logging

## Technologies Used
- Django
- Django REST Framework
- Face Recognition Library (specify which one you're using, e.g., face_recognition, OpenCV, etc.)
- SQLite (or your database of choice)

Installation

Clone the repository:
Copygit clone https://github.com/yourusername/face-recog-security.git
cd face-recog-security

Create and activate a virtual environment:
Copypython -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required packages:
Copypip install -r requirements.txt

Apply migrations:
Copypython manage.py migrate

Create a superuser:
Copypython manage.py createsuperuser

Run the development server:
Copypython manage.py runserver


API Endpoints

/api/register/: User registration
/api/login/: User login
/api/face-recognition/: Face recognition and emotion detection
/api/send-emotion-to-manager/: Send detected emotion to manager

Usage

Register a new user using the /api/register/ endpoint.
Log in using the /api/login/ endpoint to receive an authentication token.
Use the token to access the face recognition endpoint /api/face-recognition/.
The system will detect the face, recognize the emotion, and log the result.
If configured, the system will notify the manager of the detected emotion.

Configuration

Update settings.py with your specific configuration needs.
Ensure your face recognition model is properly set up and configured.
