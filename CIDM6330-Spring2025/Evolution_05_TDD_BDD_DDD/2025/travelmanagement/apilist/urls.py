from django.urls import path
from . import views

app_name = "apilist"
urlpatterns = [
    path("", views.index, name="index"),
]
