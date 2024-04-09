from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
router = SimpleRouter()
router.register(r'trafficview', views.TrafficView, basename='TrafficView')
urlpatterns = [
    path('', include(router.urls)),
]
