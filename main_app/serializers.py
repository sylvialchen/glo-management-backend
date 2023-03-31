from rest_framework import serializers
from .models import (
    Chapter,
    Job_Opps_And_Referrals,
    Sister,
    Member_Experiences,
    Position_Titles,
    Chapter_Stats,
    Events,
    Announcements,
)
from django.contrib.auth import get_user_model


class ChapterStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter_Stats
        fields = (
            "active_nb",
            "inactive_nb",
            "alumni_nb",
            "deceased_nb",
            "total_crossed_nb",
        )


class ChapterSerializer(serializers.ModelSerializer):
    chapter_status_txt = serializers.CharField(source="get_chapter_status_txt_display")
    chapter_stats = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = (
            "id",
            "associate_chapter_fg",
            "greek_letter_assigned_txt",
            "chapter_school_txt",
            "city_state_txt",
            "original_founding_date",
            "recharter_date",
            "chapter_status_txt",
            "chapter_stats",
        )

    def get_chapter_stats(self, obj):
        active_nb = len(Sister.objects.filter(chapter_nb_id=obj.id, status_txt="AC"))
        inactive_nb = len(Sister.objects.filter(chapter_nb_id=obj.id, status_txt="IA"))
        alumni_nb = len(Sister.objects.filter(chapter_nb_id=obj.id, status_txt="AL"))
        deceased_nb = len(Sister.objects.filter(chapter_nb_id=obj.id, status_txt="DE"))
        total_crossed_nb = active_nb + inactive_nb + alumni_nb + deceased_nb

        chapter_stats = Chapter_Stats(
            active_nb=active_nb,
            inactive_nb=inactive_nb,
            alumni_nb=alumni_nb,
            deceased_nb=deceased_nb,
            total_crossed_nb=total_crossed_nb,
        )

        serializer = ChapterStatsSerializer(chapter_stats)

        return serializer.data


class MemberExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Experiences
        fields = ("id", "position_nb", "start_date", "end_date", "chapter_nb")


class PositionsTitlesSerializer(serializers.ModelSerializer):
    # job_family_txt = serializers.CharField(source='get_job_family_txt_display')

    class Meta:
        model = Position_Titles
        fields = (
            "id",
            "position_title_txt",
            "active_fg",
            "e_board_fg",
            "description_txt",
            "job_family_txt",
        )


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
        fields = [
            "id",
            "first_name_txt",
            "last_name_txt",
            "nickname_txt",
            "nickname_meaning_txt",
            "chapter_nb",
            "crossing_chapter_nb",
            "crossing_class_txt",
            "crossing_date",
            "initiation_date",
            "line_nb",
            "big_sister_nb",
            "tree_txt",
            "status_txt",
            "current_city_txt",
            "current_state_txt",
            "current_country_txt",
            "email_address_txt",
            "coach_fg",
            "current_position_txt",
            "current_company_txt",
            "linkedin_url_txt",
            "expertise_interests_nb",
            "summary_txt",
            "experiences",
        ]


class ExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "member_nb")

    member_nb = SistersSerializer(many=False, read_only=True)


class JobOppsAndReferralsSerializer(serializers.ModelSerializer):
    # level_of_opening_txt = serializers.CharField(
    #     source='get_level_of_opening_txt_display')
    poster_nb = SistersSerializer(many=False, read_only=True)

    class Meta:
        model = Job_Opps_And_Referrals
        fields = (
            "id",
            "pub_date",
            "job_title_txt",
            "company_name_txt",
            "job_link_txt",
            "remote_role_fg",
            "city_txt",
            "state_txt",
            "level_of_opening_txt",
            "industry_nb",
            "description_txt",
            "poster_nb",
        )


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = (
            "id",
            "national_event",
            "name",
            "date",
            "location",
            "url",
            "description",
            "category",
            "host_chapter",
        )


class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = (
            "id",
            "national_announcement_fg",
            "chapter_announcement_nb",
            "title_txt",
            "description_txt",
            "link_txt",
            "start_posting_date",
            "end_posting_date",
            "request_date",
            "approved_fg",
        )
