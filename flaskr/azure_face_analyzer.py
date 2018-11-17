import os
import logging
import cognitive_face
from PIL import Image

logger = logging.getLogger(__name__)

FACE_API_KEY = os.getenv('FACE_API_KEY')
FACE_API_URL = os.getenv('FACE_API_URL')

cognitive_face.Key.set(FACE_API_KEY)
cognitive_face.BaseUrl.set(FACE_API_URL)

def run_the_thing(images):
    logger.info('Detecting %d images' % len(images))
    faces = {}

    for image in images:
        result = cognitive_face.face.detect(image)
        for face in result:
            if 'faceId' in face:
                face_id = face['faceId']
                image.seek(0)
                face['original_image'] = image
                faces[face_id] = face

    face_ids = list(faces.keys())
    logger.info('Grouping %d face IDs' % len(face_ids))

    if len(face_ids) < 2:
        return

    group_result = cognitive_face.face.group(face_ids)

    groups = group_result.get('groups', False)
    if not groups or len(groups) == 0:
        return
    largest_group = max(groups, key=lambda group: len(group))

    best_face_ratio = 0
    best_face = None
    for face_id in largest_group:
        face = faces[face_id]
        img = Image.open(face['original_image'])
        full_image_size = img.size[0] * img.size[1]

        face_rect = face['faceRectangle']
        face_size = face_rect['width'] * face_rect['height']

        face_ratio = face_size / full_image_size
        if face_ratio > best_face_ratio:
            best_face_ratio = face_ratio
            best_face = face

    best_face['filename'] = best_face['original_image'].filename
    best_face.pop('original_image')

    return best_face





