from django.urls import path
from .views import LoginView

urlpatterns = [
    path('user/login/', LoginView.as_view(), name='api-login'),
    path('user/register/', LoginView.as_view(), name='api-register'),
    # 其他 URL 配置...
]
