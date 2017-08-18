import os
import mimetypes

from PIL import Image

def get_image_info(image):
    image_info = dict()

    image_info['mimetype'] = mimetypes.guess_type(image)[0]
    image_info['size'] = str(os.stat(image).st_size)

    with Image.open(image) as img:
        image_info['w'] = str(img.width)
        image_info['h'] = str(img.height)

    return image_info

def prepare_image(client, image):
    img = dict()

    img['filename'] = os.path.split(image)[1]
    img['info'] = get_image_info(image)
    
    with open(image, 'rb') as pic:
        img['uri'] = client.upload(pic, img['info']['mimetype'])
    
    return img

def create_thumbnail(image):
    # TODO
    pass