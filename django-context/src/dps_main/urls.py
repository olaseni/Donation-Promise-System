from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import SimpleRouter

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe

from dps_main.views import views
from dps_main.views.viewsets import CauseViewSet, PromiseViewSet

router = SimpleRouter()

router.register(r'cause', CauseViewSet)
router.register(r'promise', PromiseViewSet)

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(template_name='dps_main/auth/register.html'), name='register'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='dps_main/auth/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(template_name='dps_main/auth/logout.html'), name='logout'),
    path('', require_safe(views.CausesListView.as_view(template_name='dps_main/user/home.html')), name='home'),
    path('make/promise/<int:pk>',
         login_required(views.CausesPromiseDetailsView.as_view(template_name='dps_main/user/make_promise.html')),
         name='make_promise'),
    path('make/promise/<int:pk>/go',
         login_required(require_POST(views.MakePromiseFormView.as_view())), name='make_promise_go'),
    path('api/', lambda request: redirect('/api/v1/', permanent=False)),
    path(r'api/v1/', include(router.urls)),
    path(r'api/v1/auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    # static media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
