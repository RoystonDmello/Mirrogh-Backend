# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from PIL import Image
import numpy as np

import os

from neural_style import mirrogh as miro
from utils import image_utils as iu
from portrait import transform as trns


class ImageTransformView(APIView):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    parser_classes = (MultiPartParser,)

    def post(self, request):

        image = request.data['image']
        style = request.data['style']

        temp = 'temp'

        path = default_storage.save(temp, ContentFile(image.read()))
        full_path = default_storage.path(path)

        if style != 'portrait':
            img_arr = iu.get_arr(full_path)

            model_path =  os.path.join(settings.STYLES_DIR, style)

            transformed =  miro.transform_img(img_arr, model_path)
            
        else:
            img = Image.open(full_path)

            transformed = trns.transform(img)

        transformed = transformed.astype('uint8')        

        img_str = iu.get_b64(transformed)

        sendable = {'image_string': img_str}

        default_storage.delete(temp)

        return Response(sendable)

class StyleListRetrieveView(APIView):

    def get(self, format=None):
        thumbs = os.listdir(settings.THUMBS_DIR)

        returnable = []

        for f in thumbs:
            returnable.append({
                "name": f.split('.')[0] + '.ckpt',
                "thumbnail": staticfiles_storage.url(settings.THUMBS + '/' + f)
            })

        return Response(returnable)