from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'auth2', views.Auth2, basename='Auth2')
router.register((r'login'), views.Login, basename='Login')

urlpatterns = [
    path('', include(router.urls)),
]