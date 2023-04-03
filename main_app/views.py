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
    MyUser
)
from .serializers import (
    ChapterSerializer,
    JobOppsAndReferralsSerializer,
    MembersSerializer,
    MemberExperiencesSerializer,
    ChapterStatsSerializer,
    EventsSerializer,
    ExtendedUserSerializer,
    PositionsTitlesSerializer,
    AnnouncementsSerializer,
)




class ExtendedUserMe(APIView):
    def get(self, request):
        serializer = ExtendedUserSerializer(request.user)
        return Response(serializer.data)


# Currently displays all users, but we will adjust this to be all users 
# that don't have an associated member model.
class MyUserList(APIView):
    def get(self, request):
        users = MyUser.objects.all()
        serializer = ExtendedUserSerializer(users, many=True)
        return Response(serializer.data)
    
    
class CoachListView(APIView):
    def get(self, request):
        data = Member.objects.filter(coach_fg=True)
        serializer = MembersSerializer(data, context={"request": request}, many=True)
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
        recent_jobs = Job_Opps_And_Referrals.objects.filter(pub_date__gte=cutoff_date)
        
        serializer = self.serializer_class(recent_jobs, many=True)
        return Response(serializer.data)
    

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
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterView(BaseViewAllApi):
    model = Chapter
    serializer_class = ChapterSerializer


class JobOppsAndReferralsView(BaseViewAllApi):
    model = Job_Opps_And_Referrals
    serializer_class = JobOppsAndReferralsSerializer


class MemberView(BaseViewAllApi):
    model = Member
    serializer_class = MembersSerializer


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
        serializer = self.serializer_class(instance, context={"request": request})
        return Response(serializer.data)

    def put(self, request, id):
        instance = self.get_object(id)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance, data=request.data, context={"request": request}
        )
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
        serializer = self.serializer_class(chapter, context={"request": request})
        # Retrieve members associated with the chapter
        members = Member.objects.filter(
            Q(chapter_nb=chapter) | Q(crossing_chapter_nb=chapter)
        )
        member_serializer = MembersSerializer(
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
    serializer_class = MembersSerializer


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
