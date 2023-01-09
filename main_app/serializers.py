from rest_framework import serializers
from .models import Chapter


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('name', 'chapter_school',
                  'city_state', 'original_founding_date')
