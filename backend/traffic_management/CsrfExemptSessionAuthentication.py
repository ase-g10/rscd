# 在你的 Django 应用的 authentication.py 中
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        # 不执行任何操作即禁用 CSRF 检查
        return
