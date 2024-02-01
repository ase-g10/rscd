from django.test import TestCase

# Create your tests here.

import requests
def test_post_location():
        url = "http://127.0.0.1:8000/dr/api/disasterview/post_location/"  # 替换为你的实际 API 端点
        data = {
            "latitude": "54",
            "longitude": "54"
        }
        response = requests.post(url, json=data)
        # 确认响应状态码为 200
        assert response.status_code == 200