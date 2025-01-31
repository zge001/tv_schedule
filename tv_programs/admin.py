from django.contrib import admin
from .models import TVChannel, TVProgram

# Register your models here.
admin.site.register(TVChannel)
admin.site.register(TVProgram)