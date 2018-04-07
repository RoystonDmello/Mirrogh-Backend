"""
This module used the DeepLabModel to perform the segmentation and returns the
result
"""


import cv2
import numpy as np

from .deeplab import DeepLabModel
import os

from django.conf import settings


memory = 'big' #big or small depending on your VRAM
model = DeepLabModel(os.path.join(settings.PORTRAIT_DIR, memory))

def transform(img):
    """
    Given an image it transforms it into the portrait mode image
    :param img: Image, input image
    :return: NUmpy array, output image
    """

    resized_image, seg_map =  model.run(img)

    resized_image = np.array(resized_image)

    blur = cv2.GaussianBlur(resized_image,(7,7),10)

    seg_map[seg_map > 0] = 1

    img_bg = np.zeros(resized_image.shape)
    img_fg = np.zeros(resized_image.shape)

    for i in range(3):
        img_fg[:,:,i] = seg_map*resized_image[:,:, i]
        img_bg[:,:,i] = np.logical_not(seg_map)*blur[:,:, i]

    final = cv2.add(img_fg, img_bg)

    return final