from django.contrib import admin

# Register your models here.
from .models import User, Disaster, Vehicle


admin.site.site_header = "Disaster Response Admin"
admin.site.register(User)
admin.site.register(Disaster)
admin.site.register(Vehicle)
