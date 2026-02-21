from django.contrib import admin

from .models import MusicRequest, Profile, RequestCategory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone')
    search_fields = ('user__username', 'full_name', 'phone')


@admin.register(RequestCategory)
class RequestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(MusicRequest)
class MusicRequestAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user', 'event_date', 'category', 'participation_format', 'status')
    list_filter = ('status', 'event_date', 'category')
    search_fields = ('project_name', 'genre', 'user__username', 'user__profile__full_name', 'category__name')
