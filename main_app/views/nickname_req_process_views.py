from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from ..models import Member_Experiences
from ..serializers import CurrentPESerializer

class CurrentPEView(APIView):
    def get(self, request, *args, **kwargs):
        # Get experiences with end_date greater than today and position_nb of 6
        today = date.today()
        experiences = Member_Experiences.objects.filter(
            end_date__gt=today,
            position_nb_id=6
        )

        # Group experiences by chapter_nb
        group_chapters = {}
        for experience in experiences:
            chapter_nb = experience.chapter_nb.id
            if chapter_nb not in group_chapters:
                group_chapters[chapter_nb] = []
            serializer = CurrentPESerializer(experience)
            group_chapters[chapter_nb].append(serializer.data)
        return Response(group_chapters, status=status.HTTP_200_OK)