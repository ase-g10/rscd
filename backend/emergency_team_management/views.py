from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from models.models import Disaster, Log
from django.http import JsonResponse
# Create your views here.
class EmergencyView(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])
    def response(self, request):
        try:
            data = request.data
            disaster_name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            location = data.get('location')
            responsible_team = data.get('username')
            print(responsible_team)
            Tmp = Disaster.objects.filter(latitude=latitude, longitude=longitude)
            for tmp in Tmp:
                create_time = tmp.create_time
            is_delete = Disaster.objects.filter(latitude=latitude, longitude=longitude)
            # if is_delete:
            #     return JsonResponse({"message": "already deleted"})
            log = Log()
            log.disaster_name = disaster_name
            log.description = description
            log.latitude = latitude
            log.longitude = longitude
            log.location = location
            log.responsible_team = responsible_team
            # log.create_time = create_time
            log.save()
            return JsonResponse({"message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)