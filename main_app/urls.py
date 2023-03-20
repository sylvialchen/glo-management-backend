from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path("api/chapters/", views.chapters_list),
    path("api/chapters/edit/<int:id>", views.chapters_detail),
    path("api/jobs/", views.jobs_list),
    path("api/sisters/", views.sisters_list),
    path("api/sisters/edit/<int:id>", views.sisters_detail),
    path("api/experiences", views.experiences_list),
    path("api/coaches", views.coach_list),
    path("api/events/", views.events_list),
    # path("user/me/", views.ExtendedUserMe, name="authemail-me"),
]
