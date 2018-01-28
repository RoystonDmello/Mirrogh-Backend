from django.conf.urls import url, include

from .views import ImageTransformView

urlpatterns = [
    url(r'^transform/$', ImageTransformView.as_view())
]