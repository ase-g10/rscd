from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
router = SimpleRouter()
router.register(r'disasterview', views.DisasterView, basename='DisasterView')
# /post_location,  /disaster_view
urlpatterns = [
    path('', include(router.urls)),
]
