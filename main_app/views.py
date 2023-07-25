from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import status
from rest_framework.views import APIView
from .model_choices import *
from . import model_choices
from .models import (
    Chapter,
    Industry,
    Chapter_Stats,
    Member,
    Pnm,
    Nickname_Request,
    Job_Opps_And_Referrals,
    Member_Experiences,
    Events,
    Position_Titles,
    Announcements,
    MyUser,
    Ethnicities,
    Dialects
)
from .serializers import (
    ChapterSerializer,
    JobOppsAndReferralsSerializer,
    MembersSerializerFull,
    MemberExperiencesSerializer,
    ChapterStatsSerializer,
    EventsSerializer,
    ExtendedUserSerializer,
    PositionsTitlesSerializer,
    AnnouncementsSerializer,
    MembersSerializerAbbr,
    EthnicitiesSerializer,
    DialectsSerializer,
    ModelChoicesSerializer
)
from django.http import JsonResponse
from django.middleware.csrf import get_token


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})


class ModelChoicesView(APIView):
    def get(self, request):
        serializer_context = {}
        for name in dir(model_choices):
            if name.isupper():
                choices = getattr(model_choices, name)
                serializer_context[name] = {
                    code: label for code, label in choices}
        serializer = ModelChoicesSerializer(data=serializer_context)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ExtendedUserMe(APIView):
    def get(self, request):
        serializer = ExtendedUserSerializer(request.user)
        return Response(serializer.data)


# Displays all users that have registered and are not assigned to a Member Profile
class UnassignedMemberList(APIView):
    serializer_class = MembersSerializerAbbr
    allow_methods = ["GET"]

    def get_queryset(self):
        queryset = Member.objects.filter(myuser__isnull=True)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        # Get unassigned users
        unassigned_users = MyUser.objects.filter(member_nb=None)
        user_serializer = ExtendedUserSerializer(unassigned_users, many=True)

        return Response(
            {
                "unassigned_users": user_serializer.data,
                "unassigned_members": serializer.data,
            }
        )


class CoachListView(APIView):
    def get(self, request):
        data = Member.objects.filter(coach_fg=True)
        serializer = MembersSerializerFull(
            data, context={"request": request}, many=True
        )
        return Response(serializer.data)


class MemberAnnouncementView(APIView):
    def get(self, request, *args, **kwargs):
        current_time = timezone.now()
        test = kwargs.get("type")
        print(type(test))
        if test == "current":
            data = Announcements.objects.filter(
                approved_fg=True,
                start_posting_date__lte=current_time,
                end_posting_date__gte=current_time,
            ).exclude(start_posting_date__isnull=True, end_posting_date__isnull=True)
        else:
            data = Announcements.objects.filter(
                approved_fg=True, end_posting_date__lte=current_time
            )

        serializer = AnnouncementsSerializer(
            data, context={"request": request}, many=True
        )
        return Response(serializer.data)


class RecentJobsAPIView(APIView):
    serializer_class = JobOppsAndReferralsSerializer

    def get(self, request):
        cutoff_date = timezone.now() - timezone.timedelta(days=30)
        recent_jobs = Job_Opps_And_Referrals.objects.filter(
            pub_date__gte=cutoff_date)

        serializer = self.serializer_class(recent_jobs, many=True)
        return Response(serializer.data)


# BaseViewAll is reusable code to get all or create 1 or more new instance(s) for aspecified model
class BaseViewAllApi(APIView):
    model = None
    serializer_class = None

    def get(self, request):
        data = self.model.objects.all()
        serializer = self.serializer_class(
            data, context={"request": request}, many=True
        )
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        if isinstance(request.data, list):
            # Handle bulk creation
            serializer = self.serializer_class(
                data=request.data, many=True, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle single creation
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Retrieve the 'poster_nb' from the request data
                poster_nb = request.data.get("poster_nb")
                # Only assign 'poster_nb' if it exists
                if poster_nb is not None:
                    try:
                        # Fetch the Member instance using the provided poster_nb
                        member = Member.objects.get(id=poster_nb)
                        serializer.validated_data["poster_nb"] = member
                    except Member.DoesNotExist:
                        # Handle the case if the Member does not exist
                        pass

                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class EthnicitiesView(BaseViewAllApi):
    model = Ethnicities
    serializer_class = EthnicitiesSerializer


class DialectsView(BaseViewAllApi):
    model = Dialects
    serializer_class = DialectsSerializer


class ChapterView(BaseViewAllApi):
    model = Chapter
    serializer_class = ChapterSerializer


class JobOppsAndReferralsView(BaseViewAllApi):
    model = Job_Opps_And_Referrals
    serializer_class = JobOppsAndReferralsSerializer


class MemberView(BaseViewAllApi):
    model = Member
    serializer_class = MembersSerializerFull


class MemberExperiencesView(BaseViewAllApi):
    model = Member_Experiences
    serializer_class = MemberExperiencesSerializer


class EventsView(BaseViewAllApi):
    model = Events
    serializer_class = EventsSerializer


class PositionsAndTitlesView(BaseViewAllApi):
    model = Position_Titles
    serializer_class = PositionsTitlesSerializer


class AnnouncementsView(BaseViewAllApi):
    model = Announcements
    serializer_class = AnnouncementsSerializer

# BaseDetail is reusable code to get, update or delete the detail of single instance


class BaseDetailView(APIView):
    model = None
    serializer_class = None

    # get_object is a helper function for all the methods listed after
    def get_object(self, id):
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None

    def get(self, request, id):
        instance = self.get_object(id)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance, context={"request": request})
        return Response(serializer.data)

    def put(self, request, id):
        instance = self.get_object(id)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance, data=request.data, context={"request": request}, partial=True
        )
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        instance = self.get_object(id)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChapterDetailView(BaseDetailView):
    model = Chapter
    serializer_class = ChapterSerializer

    def get(self, request, id):
        chapter = self.model.objects.get(id=id)
        serializer = self.serializer_class(
            chapter, context={"request": request})
        # Retrieve members associated with the chapter
        members = Member.objects.filter(
            Q(chapter_nb=chapter) | Q(crossing_chapter_nb=chapter)
        )
        member_serializer = MembersSerializerFull(
            members, many=True, context={"request": request}
        )
        data = serializer.data
        # Add members data to the response
        data["members"] = member_serializer.data
        return Response(data)


class JobOppsAndReferralsDetailView(BaseDetailView):
    model = Job_Opps_And_Referrals
    serializer_class = JobOppsAndReferralsSerializer


class MemberDetailView(BaseDetailView):
    model = Member
    serializer_class = MembersSerializerFull


class MemberExperiencesDetailView(BaseDetailView):
    model = Member_Experiences
    serializer_class = MemberExperiencesSerializer


class EventsDetailView(BaseDetailView):
    model = Events
    serializer_class = EventsSerializer


class PositionsAndTitlesDetailView(BaseDetailView):
    model = Position_Titles
    serializer_class = PositionsTitlesSerializer


class AnnouncementsDetailView(BaseDetailView):
    model = Announcements
    serializer_class = AnnouncementsSerializer
