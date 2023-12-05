from django.contrib import admin
from .models import User

# Register your models here.
admin.site.site_header = "Disaster Response Admin"
admin.site.site_title = "Disaster Response Admin Portal"
admin.site.index_title = "Welcome to Disaster Response Portal"

admin.site.register(User)
