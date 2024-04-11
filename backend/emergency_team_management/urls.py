from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
router = SimpleRouter()
router.register(r'emergencyview', views.EmergencyView, basename='EmergencyView')
urlpatterns = [
    path('', include(router.urls)),
]
