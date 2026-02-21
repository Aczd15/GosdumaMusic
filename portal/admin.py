from django.contrib import admin

from .models import MusicGroup, MusicRequest, Profile, RequestCategory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'group')
    search_fields = ('user__username', 'full_name', 'phone', 'group__name')


@admin.register(MusicGroup)
class MusicGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')


@admin.register(RequestCategory)
class RequestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(MusicRequest)
class MusicRequestAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user', 'event_date', 'category', 'participation_format', 'status')
    list_filter = ('status', 'event_date', 'category')
    search_fields = ('project_name', 'genre', 'user__username', 'user__profile__full_name', 'category__name')
