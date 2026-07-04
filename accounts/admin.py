from django.contrib import admin
from .models import UserHealth


@admin.register(UserHealth)
class UserHealthAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'mobile',
        'age',
        'gender',
        'height',
        'weight',
        'goal',
        'activity_level',
    )

    search_fields = ('user__username', 'mobile')
    list_filter = ('gender', 'goal')