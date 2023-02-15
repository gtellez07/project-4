from django.contrib import admin

from .models import Show, Series


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'description', 'review')

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'description', 'show_id', 'user_id', 'favorite', 'watched', 'review')


