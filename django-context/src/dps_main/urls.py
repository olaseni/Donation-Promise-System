from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from dps_main.views.viewsets import ContactViewSet, CauseViewSet, PromiseViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'cause', CauseViewSet)

router.register(r'promise', PromiseViewSet)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    # static media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
