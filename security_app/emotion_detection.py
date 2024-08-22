from deepface import DeepFace
import cv2

def detect_emotion(image_path):
    try:
        # Analyze the image using DeepFace
        result = DeepFace.analyze(image_path, actions=['emotion'])
        
        # Get the dominant emotion
        emotion = result[0]['dominant_emotion']
        return emotion
    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
        return "unknown"

# Example usage
if __name__ == "__main__":
    test_image_path = "path/to/test/image.jpg"
    detected_emotion = detect_emotion(test_image_path)
    print(f"Detected emotion: {detected_emotion}")