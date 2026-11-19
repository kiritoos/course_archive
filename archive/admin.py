from django.contrib import admin
from .models import Work, Discipline, Keyword

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "supervisor", "discipline", "grade", "is_defended")
    list_filter = ("is_defended", "year", "discipline")
    search_fields = ("title", "supervisor")

admin.site.register(Discipline)
admin.site.register(Keyword)