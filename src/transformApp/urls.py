from django.conf.urls import url, include

from .views import ImageTransformView, StyleListRetrieveView

urlpatterns = [
    url(r'^transform/$', ImageTransformView.as_view()),
    url(r'^styles/get/$', StyleListRetrieveView.as_view())
]