from django.urls import path
from .views import (
    ChapterView,
    ChapterDetailView,
    JobOppsAndReferralsView,
    JobOppsAndReferralsDetailView,
    SisterView,
    SisterDetailView,
    MemberExperiencesView,
    MemberExperiencesDetailView,
    EventsView,
    EventsDetailView,
    PositionsAndTitlesView,
    PositionsAndTitlesDetailView,
    ExtendedUserMe,
    # coach_list,
    CoachListView,
)

urlpatterns = [
    # Following paths accept:
    # "GET" call to find user-specific data:
    path("user/me/", ExtendedUserMe.as_view(), name="extended-user-me"),
    # Following paths accept:
    # "GET" API calls to find list of ALL
    path("api/coaches/", CoachListView.as_view),
    # Following paths accept:
    # "GET" API calls to find list of ALL
    # "POST" calls to add to database/list
    path("api/chapters/", ChapterView.as_view(), name="chapter-list"),
    path(
        "api/jobs/",
        JobOppsAndReferralsView.as_view(),
        name="job-opps-and-referrals-list",
    ),
    path("api/members/", SisterView.as_view(), name="sister-list"),
    path(
        "api/experiences/",
        MemberExperiencesView.as_view(),
        name="member-experiences-list",
    ),
    path(
        "api/positionsandtitles/",
        PositionsAndTitlesView.as_view(),
        name="positions-and-titles-list",
    ),
    path("api/events/", EventsView.as_view(), name="events-list"),
    # Following paths accept:
    # "GET" calls to get detail view
    # "PUT" calls to update specific ID
    # "DELETE" calls to delete
    path("api/chapters/<int:id>/", ChapterDetailView.as_view(), name="chapter-detail"),
    path(
        "api/jobs/<int:id>",
        JobOppsAndReferralsDetailView.as_view(),
        name="job-opps-and-referrals-detail",
    ),
    path("api/members/<int:id>", SisterDetailView.as_view(), name="sister-detail"),
    path(
        "api/experiences/<int:id>",
        MemberExperiencesDetailView.as_view(),
        name="member-experiences-detail",
    ),
    path(
        "api/positionsandtitles/<int:id>",
        PositionsAndTitlesDetailView.as_view(),
        name="positions-and-titles-detail",
    ),
    path("api/events/<int:id>", EventsDetailView.as_view(), name="events-detail"),
]
