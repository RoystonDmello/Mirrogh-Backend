# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
import base64
import cStringIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from PIL import Image
import numpy as np

import os

from neural_style import mirrogh as miro

class ImageTransformView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):

        image = request.data['image']

        temp = 'temp'

        path = default_storage.save(temp, ContentFile(image.read()))
        full_path = default_storage.path(path)

        img = Image.open(full_path)

        width, height = img.size

        required_height = 1300

        if height > required_height:
            ratio = float(width)/height

            img = img.resize((int(ratio*required_height), required_height), Image.ANTIALIAS)
        print img.size

        img_array = np.array(img)

        base = settings.BASE_DIR
        rel_model_path = 'models/scream.ckpt'
        model_path =  os.path.join(base, rel_model_path)

        print(model_path)

        transformed =  miro.transform_img(img_array, model_path)
        transformed = transformed.astype('uint8')        

        img_new = Image.fromarray(transformed)

        buffer = cStringIO.StringIO()
        img_new.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue())

        sendable = {'image_string': img_str}

        return Response(sendable)


        