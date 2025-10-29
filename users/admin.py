from django.contrib import admin
from .models import LinkItem

@admin.register(LinkItem)
class LinkItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tipo", "url", "created_at")
    search_fields = ("url", "user__username")
    list_filter = ("tipo",)

