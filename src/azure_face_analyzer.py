import os
import logging
import cognitive_face
from PIL import Image
import viz_exceptions

logger = logging.getLogger(__name__)

FACE_API_KEY = os.getenv('FACE_API_KEY')
FACE_API_URL = os.getenv('FACE_API_URL')

cognitive_face.Key.set(FACE_API_KEY)
cognitive_face.BaseUrl.set(FACE_API_URL)

def find_most_common_face(images):
    if not images or len(images) == 1:
        raise viz_exceptions.MustUploadImagesException()

    faces = detect_faces(images)
    face_ids_by_person = group_faces_by_person(faces)
    largest_group_of_face_ids = find_largest_group(face_ids_by_person)
    faces_of_most_common_person = [faces[face_id] for face_id in largest_group_of_face_ids]
    best_face = get_best_face_in_group(faces_of_most_common_person)

    if not best_face:
        raise viz_exceptions.NoCommonFace()

    return best_face


def detect_faces(images):
    logger.info('Detecting %d images' % len(images))
    faces = {}

    for image in images:
        result = cognitive_face.face.detect(image)
        for face in result:
            if 'faceId' in face:
                face_id = face['faceId']
                face['original_image'] = image
                faces[face_id] = face

    if not faces:
        raise viz_exceptions.NoFacesException()

    return faces


def group_faces_by_person(faces):
    face_ids = list(faces.keys())
    logger.info('Grouping %d face IDs' % len(face_ids))

    if len(face_ids) == 1:
        return face_ids

    group_result = cognitive_face.face.group(face_ids)
    groups = group_result.get('groups', [])
    return groups


def find_largest_group(groups):
    if not groups:
        return []
    return max(groups, key=lambda group: len(group))


def get_best_face_in_group(faces):
    if not faces:
        return None
    return max(faces, key=get_face_to_image_ratio)


def get_face_to_image_ratio(face):
    face['original_image'].seek(0)
    img = Image.open(face['original_image'])
    full_image_size = img.size[0] * img.size[1]

    face_rect = face['faceRectangle']
    face_size = face_rect['width'] * face_rect['height']

    return (face_size / full_image_size)
