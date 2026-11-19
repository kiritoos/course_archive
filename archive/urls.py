from django.urls import path
from . import views

app_name = "archive"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.work_create, name="create"),
    path("<int:pk>/edit/", views.work_update, name="update"),
    path("<int:pk>/delete/", views.work_delete, name="delete"),
    path("search/", views.search, name="search"),
    path("stats/", views.stats, name="stats"),
]