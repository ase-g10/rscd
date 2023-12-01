from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


# from .serializers import ItemSerializer

# Create your views here.
# def post_location(request):
#
#     return JsonResponse({"message": "OK"})


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # 禁用 CSRF 令牌，以便于测试（在实际部署中应该启用 CSRF 保护）
@require_http_methods(["POST"])  # 仅允许 POST 请求
def post_location(request):
    try:
        # 将请求的 JSON 转换成 Python 字典
        data = json.loads(request.body)

        # 提取纬度和经度数据
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # 在这里处理数据（例如，保存到数据库或执行其他操作）

        # 返回成功响应
        return JsonResponse({"status": "success", "message": "Location received successfully."})
    except json.JSONDecodeError:
        # 如果请求的内容不是有效的 JSON，返回错误响应
        return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
    except Exception as e:
        # 处理其他意外错误
        return JsonResponse({"status": "error", "message": str(e)}, status=500)