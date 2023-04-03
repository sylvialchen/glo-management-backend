from rest_framework import serializers
from django.db.models import Count, Min, Max, Avg
from .models import (
    Chapter,
    Job_Opps_And_Referrals,
    Member,
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
            "memorial_nb",
            "total_crossed_nb",
            "smallest_class_crossed_nb",
            "largest_class_crossed_nb",
            "average_class_crossed_fl",
        )


class MemberExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Experiences
        fields = ("id", "member_nb", "position_nb", "start_date", "end_date", "chapter_nb")


class MembersSerializer(serializers.ModelSerializer):
    # crossing_class_txt = serializers.CharField(
    #     source='get_crossing_class_txt_display')
    # status_txt = serializers.CharField(source='get_status_txt_display')
    # chapter_nb = ChapterSerializer(many=False, read_only=True)
    experiences = MemberExperiencesSerializer(many=True, read_only=True)
    # StringRelatedField calls the __str__ method on the corresponding model
    # i.e., Chapter_nb is a FK to Chapter
    # chapter_nb = serializers.StringRelatedField(many=False)

    class Meta:
        model = Member
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
            "big_nb",
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


class ChapterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    chapter_status_txt = serializers.CharField(source="get_chapter_status_txt_display")
    chapter_stats = serializers.SerializerMethodField()
    members = MembersSerializer(many=True, read_only=True)

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
            "members"
        )

    def get_chapter_stats(self, obj):
        member_counts = Member.objects.filter(chapter_nb_id=obj.id).values('crossing_class_txt').annotate(count=Count('id'))
        class_counts = {mc['crossing_class_txt']: mc['count'] for mc in member_counts}
        counts = list(class_counts.values())
        active_nb = len(Member.objects.filter(chapter_nb_id=obj.id, status_txt="AC"))
        inactive_nb = len(Member.objects.filter(chapter_nb_id=obj.id, status_txt__in=["IM", "IN", "PI"]))
        alumni_nb = len(Member.objects.filter(chapter_nb_id=obj.id, status_txt="AL"))
        memorial_nb = len(Member.objects.filter(chapter_nb_id=obj.id, status_txt="ME"))
        total_crossed_nb = active_nb + inactive_nb + alumni_nb + memorial_nb
        if class_counts:
            smallest_class_crossed_nb = min(class_counts, key=class_counts.get)
            largest_class_crossed_nb = max(class_counts, key=class_counts.get)
            average_class_crossed_fl = sum(class_counts.values()) / len(class_counts)
        else:
            smallest_class_crossed_nb = None
            largest_class_crossed_nb = None
            average_class_crossed_fl = None

        chapter_stats = Chapter_Stats(
            active_nb=active_nb,
            inactive_nb=inactive_nb,
            alumni_nb=alumni_nb,
            memorial_nb=memorial_nb,
            total_crossed_nb=total_crossed_nb,
            smallest_class_crossed_nb=smallest_class_crossed_nb,
            largest_class_crossed_nb=largest_class_crossed_nb,
            average_class_crossed_fl=average_class_crossed_fl
        )

        serializer = ChapterStatsSerializer(chapter_stats)

        return serializer.data


class PositionsTitlesSerializer(serializers.ModelSerializer):
    # job_family_txt = serializers.CharField(source='get_job_family_txt_display')

    class Meta:
        model = Position_Titles
        fields = '__all__'


class ExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ("email", "first_name", "last_name", "member_nb")

    member_nb = MembersSerializer(many=False, read_only=True)


class JobOppsAndReferralsSerializer(serializers.ModelSerializer):
    # level_of_opening_txt = serializers.CharField(
    #     source='get_level_of_opening_txt_display')
    poster_nb = MembersSerializer(many=False, read_only=True)

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
        fields = '__all__'


class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = '__all__'
