from django.urls import path
from .views import LoginView

urlpatterns = [
    path('user/login/', LoginView.as_view(), name='api-login'),
    # 其他 URL 配置...
]
