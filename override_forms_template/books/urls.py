from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.process_form, name="create"),
    path("<str:slug>/", views.detail, name="detail"),
    path("<str:slug>/edit/", views.process_form, name="update"),
    path("<str:slug>/delete/", views.delete, name="delete"),
]
