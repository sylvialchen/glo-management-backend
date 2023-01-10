from rest_framework import serializers
from .models import Chapter, Job_Opps_And_Referrals, Sister


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('associate_chapter', 'greek_letter_assigned', 'chapter_school',
                  'city_state', 'original_founding_date', 'recharter_date', 'chapter_status')


class JobOppsAndReferralsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_Opps_And_Referrals
        fields = ('pub_date', 'job_title', 'company_name',
                  'job_link', 'level_of_opening', 'industry', 'description', 'poster')


class SistersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sister
        fields = ('first_name', 'last_name', 'nickname',
                  'nickname_meaning', 'chapter', 'crossing_chapter', 'crossing_class', 'crossing_date', 'initiation_date', 'line_number', 'big_sister', 'tree', 'status',
                  'current_city', 'current_state', 'current_country', 'email_address',
                  'coach', 'current_position', 'current_company', 'linkedin_url',
                  'expertise_interests', 'summary')
