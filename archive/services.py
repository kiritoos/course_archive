from django.core.cache import cache
from django.db.models import Count, Avg
from .models import Discipline

STATS_KEY = "discipline_stats"

def get_discipline_stats():
    return cache.get_or_set(
        STATS_KEY,
        lambda: list(Discipline.objects.annotate(
            works_count=Count("works"),
            avg_grade=Avg("works__grade")
        ).order_by("-works_count")),
        timeout=600,
    )