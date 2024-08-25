# Face Recognition Security System

## Overview
This project is a Face Recognition Security System built with Django and Django REST Framework. It provides a robust API for user registration, authentication, and emotion detection through facial recognition.

## Features
- User registration and authentication
- Face detection and emotion recognition
- Real-time emotion logging
- Manager notification system for detected emotions

## Technologies Used
- Django
- Django REST Framework
- Face Recognition Library (specify which one you're using, e.g., face_recognition, OpenCV, etc.)
- SQLite (or your database of choice)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/face-recog-security.git
   cd face-recog-security
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `/api/register/`: User registration
- `/api/login/`: User login
- `/api/face-recognition/`: Face recognition and emotion detection
- `/api/send-emotion-to-manager/`: Send detected emotion to manager

## Usage

1. Register a new user using the `/api/register/` endpoint.
2. Log in using the `/api/login/` endpoint to receive an authentication token.
3. Use the token to access the face recognition endpoint `/api/face-recognition/`.
4. The system will detect the face, recognize the emotion, and log the result.
5. If configured, the system will notify the manager of the detected emotion.

## Configuration

- Update `settings.py` with your specific configuration needs.
- Ensure your face recognition model is properly set up and configured.
