from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ApplicationUser)

class ApplicationUser(admin.ModelAdmin):
    list_display=[
        'username','choice_of_convo_remembering'
    ]