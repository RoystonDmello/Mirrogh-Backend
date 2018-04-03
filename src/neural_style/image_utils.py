"""
Utility functions for handling images
"""
import base64
import io

import numpy as np
from PIL import Image


def get_arr(full_path):
    """
    Given the path it opens the image and returns the image array needed for
    prediction
    :param full_path: String, absolute path of image
    :return: Numpy array, array of image
    """
    img = Image.open(full_path)

    width, height = img.size

    required_height = 1300

    if height > required_height:
        ratio = float(width) / height

        img = img.resize((int(ratio * required_height), required_height),
                         Image.ANTIALIAS)
    print(img.size)

    img_array = np.array(img)

    return img_array

def get_b64(img_arr):
    """
    Given an image array it converts it into
    :param img_arr: Numpy array, image array
    :return: String, base64 encoded string of the image
    """
    img_new = Image.fromarray(img_arr)

    buffer = io.BytesIO()
    img_new.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())

    return img_str