from django.urls import path
from .views import RegistrationView, LoginView, FaceRecognitionView, SendEmotionToManagerView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('face-recognition/', FaceRecognitionView.as_view(), name='face_recognition'),
    path('send-emotion-to-manager/', SendEmotionToManagerView.as_view(), name='send_emotion_to_manager'),
]