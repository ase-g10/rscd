from django.contrib import admin
from .models import User, Disaster

# Register your models here.
admin.site.register(User)
admin.site.site_header = "Disaster Response Admin"

admin.site.register(Disaster)
