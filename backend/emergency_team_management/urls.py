from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
]
