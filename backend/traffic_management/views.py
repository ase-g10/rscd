from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from models.models import DrivingLocation


class TrafficView(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def get_driving_location(self, request):
        locations = DrivingLocation.objects.filter(is_disabled=False)
        locations_list = [{"username": loc.username, "latitude": loc.latitude, "longitude": loc.longitude} for loc in locations]
        return JsonResponse({"status": "success","locations": locations_list})


    @action(detail=False, methods=['post'])
    def save_driving_location(self, request):
        username = request.data.get("username")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        if username is None or latitude is None or longitude is None:
            return JsonResponse({"status": "error", "message": "Invalid request."})
        DrivingLocation.objects.create()
        return JsonResponse({"status": "success", "message": "Location saved successfully."})