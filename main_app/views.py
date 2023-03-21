from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
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
    Sister,
    Pnm,
    Nickname_Request,
    Job_Opps_And_Referrals,
    Member_Experiences,
    Events,
    Position_Titles,
)
from .serializers import (
    ChapterSerializer,
    JobOppsAndReferralsSerializer,
    SistersSerializer,
    MemberExperiencesSerializer,
    ChapterStatsSerializer,
    EventsSerializer,
    ExtendedUserSerializer,
    PositionsTitlesSerializer,
)


class ExtendedUserMe(APIView):
    def get(self, request):
        serializer = ExtendedUserSerializer(request.user)
        return Response(serializer.data)


class CoachListView(APIView):
    def get(self, request):
        data = Sister.objects.filter(coach_fg=True)
        serializer = SistersSerializer(data, context={"request": request}, many=True)
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


class SisterView(BaseViewAllApi):
    model = Sister
    serializer_class = SistersSerializer


class MemberExperiencesView(BaseViewAllApi):
    model = Member_Experiences
    serializer_class = MemberExperiencesSerializer


class EventsView(BaseViewAllApi):
    model = Events
    serializer_class = EventsSerializer


class PositionsAndTitlesView(BaseViewAllApi):
    model = Position_Titles
    serializer_class = PositionsTitlesSerializer


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


class JobOppsAndReferralsDetailView(BaseDetailView):
    model = Job_Opps_And_Referrals
    serializer_class = JobOppsAndReferralsSerializer


class SisterDetailView(BaseDetailView):
    model = Sister
    serializer_class = SistersSerializer


class MemberExperiencesDetailView(BaseDetailView):
    model = Member_Experiences
    serializer_class = MemberExperiencesSerializer


class EventsDetailView(BaseDetailView):
    model = Events
    serializer_class = EventsSerializer


class PositionsAndTitlesDetailView(BaseDetailView):
    model = Position_Titles
    serializer_class = PositionsTitlesSerializer
