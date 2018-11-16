import os
import cognitive_face

FACE_API_KEY = os.getenv('FACE_API_KEY')
FACE_API_URL = os.getenv('FACE_API_URL')

cognitive_face.Key.set(FACE_API_KEY)
cognitive_face.BaseUrl.set(FACE_API_URL)

def recognize_face(image):
  return cognitive_face.face.detect(image)
