from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
router = SimpleRouter()
router.register(r'disasterview', views.DisasterView, basename='DisasterView')

urlpatterns = [
    path('', include(router.urls)),
]
