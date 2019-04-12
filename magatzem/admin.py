from django.contrib import admin
from .models.container import Container
from .models.task import Task
from .models.room import Room
# Register your models here.

admin.site.register(Container)
admin.site.register(Task)
admin.site.register(Room)