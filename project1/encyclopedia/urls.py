from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/add", views.addEntry, name="add"),
    path("wiki/<str:title>", views.title, name="title"),
]
