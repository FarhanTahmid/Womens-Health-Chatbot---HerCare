from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(UserConversationThreads)
class UserConversationThreads(admin.ModelAdmin):
    list_display=[
        'username','thread_id'
    ]

