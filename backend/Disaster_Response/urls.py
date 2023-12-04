from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register(r'api/disasterview', views.DisasterView, basename='DisasterView')
router.register(r'api/auth2', views.Auth2, basename='Auth2')

urlpatterns = [
    path('', include(router.urls)),
]
