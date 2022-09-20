from django.contrib import admin
from .models import Chatroom, Message

# Register your models here.


@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created")
    list_filter = ("created",)
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "room", "created")
    list_filter = ("created",)
