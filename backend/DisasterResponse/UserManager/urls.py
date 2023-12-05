from django.urls import path
from .views import *

urlpatterns = [
    path('', redirect_to_index),  # Redirect from root URL
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]