from rest_framework import serializers
from .models import User
import base64
import uuid
from django.core.files.base import ContentFile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'face_image')
        extra_kwargs = {'face_image': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            face_image=validated_data['face_image']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    

class FaceRecognitionSerializer(serializers.Serializer):
    image = serializers.CharField()
    user_id = serializers.IntegerField()

    def validate_image(self, value):
        if ';base64,' in value:
            header, image_data = value.split(';base64,')
        else:
            image_data = value
        
        try:
            decoded_file = base64.b64decode(image_data)
        except TypeError:
            raise serializers.ValidationError("Invalid image.")
        
        # Generate file name
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file extension
        file_extension = self.get_file_extension(file_name, decoded_file)
        complete_file_name = "%s.%s" % (file_name, file_extension, )
        
        data = ContentFile(decoded_file, name=complete_file_name)
        return data

    def get_file_extension(self, file_name, decoded_file):
        import imghdr
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension