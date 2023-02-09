from rest_framework import serializers
from .models import Chapter, Job_Opps_And_Referrals, Sister, Member_Experiences, Position_Titles


class ChapterSerializer(serializers.ModelSerializer):
    # chapter_status_txt = serializers.CharField(
    #     source='get_chapter_status_txt_display')

    class Meta:
        model = Chapter
        fields = ('id', 'associate_chapter_fg', 'greek_letter_assigned_txt', 'chapter_school_txt',
                  'city_state_txt', 'original_founding_date', 'recharter_date', 'chapter_status_txt')


class MemberExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Experiences
        fields = ('id', 'position_nb', 'start_date', 'end_date',
                  'chapter_nb')


class PositionsTitlesSerializer(serializers.ModelSerializer):
    # job_family_txt = serializers.CharField(source='get_job_family_txt_display')

    class Meta:
        model = Position_Titles
        fields = ('id', 'position_title_txt', 'active_fg', 'e_board_fg',
                  'description_txt', 'job_family_txt')


class SistersSerializer(serializers.ModelSerializer):
    # crossing_class_txt = serializers.CharField(
    #     source='get_crossing_class_txt_display')
    # status_txt = serializers.CharField(source='get_status_txt_display')
    # chapter_nb = ChapterSerializer(many=False, read_only=True)
    crossing_chapter_nb = ChapterSerializer(many=False, read_only=True)
    experiences = MemberExperiencesSerializer(many=True, read_only=True)
    # StringRelatedField calls the __str__ method on the corresponding model
    # i.e., Chapter_nb is a FK to Chapter
    # chapter_nb = serializers.StringRelatedField(many=False)

    class Meta:
        model = Sister
        fields = ['id', 'first_name_txt', 'last_name_txt', 'nickname_txt',
                  'nickname_meaning_txt', 'chapter_nb', 'crossing_chapter_nb',
                  'crossing_class_txt', 'crossing_date', 'initiation_date',
                  'line_nb', 'big_sister_nb', 'tree_txt', 'status_txt',
                  'current_city_txt', 'current_state_txt', 'current_country_txt',
                  'email_address_txt', 'coach_fg', 'current_position_txt',
                  'current_company_txt', 'linkedin_url_txt',
                  'expertise_interests_nb', 'summary_txt', 'experiences']


class JobOppsAndReferralsSerializer(serializers.ModelSerializer):
    # level_of_opening_txt = serializers.CharField(
    #     source='get_level_of_opening_txt_display')
    poster_nb = SistersSerializer(many=False, read_only=True)

    class Meta:
        model = Job_Opps_And_Referrals
        fields = ('id', 'pub_date', 'job_title_txt', 'company_name_txt',
                  'job_link_txt', 'remote_role_fg', 'city_txt', 'state_txt',
                  'level_of_opening_txt', 'industry_nb', 'description_txt', 'poster_nb')
