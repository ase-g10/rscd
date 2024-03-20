from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'auth2', views.Auth2, basename='auth2')
router.register((r'auth'), views.Authentication, basename='auth')
router.register(r'user_info', views.UserInfo, basename='user_info')

urlpatterns = [
    path('', include(router.urls)),
]