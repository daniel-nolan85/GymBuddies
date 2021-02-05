from django.contrib import admin

from .models import Area, Type, Exercise, Workout


admin.site.register(Area)
admin.site.register(Type)
admin.site.register(Exercise)
admin.site.register(Workout)
