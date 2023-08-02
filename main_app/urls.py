from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from .views.views import (
    ChapterView,
    ChapterDetailView,
    JobOppsAndReferralsView,
    JobOppsAndReferralsDetailView,
    MemberView,
    MemberDetailView,
    MemberExperiencesView,
    MemberExperiencesDetailView,
    EventsView,
    EventsDetailView,
    PositionsAndTitlesView,
    PositionsAndTitlesDetailView,
    ExtendedUserMe,
    CoachListView,
    AnnouncementsView,
    AnnouncementsDetailView,
    MemberAnnouncementView,
    RecentJobsAPIView,
    UnassignedMemberList,
    EthnicitiesView,
    DialectsView,
    ModelChoicesView,
)
from .views.nickname_req_process_views import (
    CurrentPEView
)
from django.http import HttpResponse
from rest_framework.authtoken.views import obtain_auth_token
from .payment_processing import create_payment_intent

urlpatterns = [
    path('api-auth/csrf/', csrf_exempt(lambda request: HttpResponse(status=204))),
    path("create-payment-intent/", create_payment_intent, name='create-payment-intent'),
    # "GET" call to find user-specific data:
    path("user/me/", ExtendedUserMe.as_view(), name="extended-user-me"),
    path("users/unassigned/", UnassignedMemberList.as_view()),
    # "GET" call to either "current" or "past" find time-sorted data:
    path(
        "api/announcements/<str:type>/",
        MemberAnnouncementView.as_view(),
        name="current_member_announcements",
    ),
    path(
        "api/jobs/recent/",
        RecentJobsAPIView.as_view(),
        name="job-opps-and-referrals-list",
    ),
    # "GET" API calls to find list of ALL
    path('api/model_choices/', ModelChoicesView.as_view(), name='model_choices'),
    path("api/coaches/", CoachListView.as_view()),
    # Following paths accept:
    # "GET" API calls to find list of ALL
    # "POST" calls to add to database/list
    path("api/chapters/", ChapterView.as_view(), name="chapter-list"),
    path(
        "api/jobs/",
        JobOppsAndReferralsView.as_view(),
        name="job-opps-and-referrals-list",
    ),
    path("api/members/", MemberView.as_view(), name="member-list"),
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
    path("api/announcements/", AnnouncementsView.as_view(), name="announcements-list"),
    path("api/ethnicities/", EthnicitiesView.as_view(), name="ethnicities-list"),
    path("api/dialects/", DialectsView.as_view(), name="dialects-list"),
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
    path("api/members/<int:id>", MemberDetailView.as_view(), name="member-detail"),
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
    path(
        "api/announcements/<int:id>",
        AnnouncementsDetailView.as_view(),
        name="announcements-detail",
    ),
# nickname request process application routes
     path("api/process_educators/now", CurrentPEView.as_view(), name="current-PEs"),
]

