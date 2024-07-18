from django.contrib import admin

# Register your models here.
from .models import Rushee, Filing

admin.site.register(Rushee)
admin.site.register(Filing)