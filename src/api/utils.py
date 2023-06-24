import os
import hashlib

from django.conf import settings
import resizer.logs
from . import models


def parse_filename(filename):
    return os.path.splitext(filename)


def get_resized_image_or_none(image_hash, width, height):
    saved_image = models.Image.objects.filter(hash=image_hash, width=width, height=height).first()
    if saved_image is None:
        resizer.logs.debug(
            'Save new image',
            hash=image_hash, width=width, height=height
        )
        models.Image.objects.create(hash=image_hash, width=width, height=height)
        return None
    else:
        resizer.logs.debug(
            'Image already resized',
            hash=image_hash, width=width, height=height
        )
        return saved_image.path


def get_height(size, width):
    ratio = size[0] / size[1]
    return round(width / ratio)


def get_resized_file_path(name, extension, width, height):
    md5 = hashlib.md5(name.encode('utf-8')).hexdigest()
    return str(os.path.join(
        settings.BASE_DIR,
        settings.RESIZED_IMAGE_FOLDER,
        f'{md5}_{width}x{height}{extension}'
    ))
