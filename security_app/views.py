from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, FaceRecognitionSerializer
from .models import User, FaceEncoding
from .face_recognition_utils import get_face_encoding, compare_faces
import numpy as np
from .emotion_detection import detect_emotion
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import os
from datetime import datetime

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            face_image_path = user.face_image.path
            face_encoding = get_face_encoding(face_image_path)
            if face_encoding is not None:
                FaceEncoding.objects.create(user=user, encoding=face_encoding.tobytes())
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response({"error": "No face detected in the image"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendEmotionToManagerView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        emotion = request.data.get('emotion')
        
        # Here you would implement the logic to send the emotion to the manager
        # This could involve saving to a database, sending an email, etc.
        
        # For demonstration, we'll just print it
        print(f"User {user_id} logged in with emotion: {emotion}")
        
        return Response({"message": "Emotion sent to manager"}, status=status.HTTP_200_OK)
        
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], 
                                password=serializer.validated_data['password'])
            if user:
                return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FaceRecognitionView(APIView):
    def post(self, request):
        image_data = request.data.get('image')
        user_id = request.data.get('user_id')
        
        if not image_data or not user_id:
            return Response({"error": "Missing image or user_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Save the captured image
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captured_{user_id}_{timestamp}.{ext}"
        data = ContentFile(base64.b64decode(imgstr), name=filename)
        
        # Save the image in the 'captured_images' folder within MEDIA_ROOT
        image_path = os.path.join(settings.MEDIA_ROOT, 'captured_images', filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb') as f:
            f.write(data.read())
        
        # Perform face recognition
        unknown_encoding = get_face_encoding(image_path)
        
        if unknown_encoding is None:
            return Response({"error": "No face detected in the image"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            face_encoding = FaceEncoding.objects.get(user=user)
            known_encoding = np.frombuffer(face_encoding.encoding, dtype=np.float64)
            
            if compare_faces(known_encoding, unknown_encoding):
                # Perform emotion detection
                emotion = detect_emotion(image_path)
                
                # Update user's latest captured image
                user.latest_captured_image.save(filename, data)
                user.save()
                
                return Response({
                    "message": "Face recognized",
                    "user_id": user.id,
                    "emotion": emotion
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Face not recognized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except FaceEncoding.DoesNotExist:
            return Response({"error": "Face encoding not found for user"}, status=status.HTTP_404_NOT_FOUND)