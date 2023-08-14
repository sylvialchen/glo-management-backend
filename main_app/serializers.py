from rest_framework import serializers
from django.db.models import Count, Min, Max, Avg
from . import model_choices
from .models import (
    Chapter,
    Job_Opps_And_Referrals,
    Member,
    Member_Experiences,
    Position_Titles,
    Chapter_Stats,
    Events,
    Announcements,
    Ethnicities,
    Dialects
)
from django.contrib.auth import get_user_model
from django.db.models import Q


class StatusTupleSerializer(serializers.Serializer):
    code = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_code(self, obj):
        return obj[0]

    def get_label(self, obj):
        return obj[1]
    
    def to_internal_value(self, data):
        if not isinstance(data, tuple) or len(data) != 2:
            self.fail('invalid')
        return {'code': data[0], 'label': data[1]}

    def to_representation(self, value):
        return (value['code'], value['label'])

    
class ModelChoicesSerializer(serializers.Serializer):
    STATUS = serializers.DictField(child=serializers.CharField())
    CHAPTER_STATUS = serializers.DictField(child=serializers.CharField())
    NICKNAME_STATUS = serializers.DictField(child=serializers.CharField())
    GREEK_CLASS = serializers.DictField(child=serializers.CharField())
    JOB_LEVEL = serializers.DictField(child=serializers.CharField())
    JOB_FAMILY = serializers.DictField(child=serializers.CharField())
    EVENT = serializers.DictField(child=serializers.CharField())


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
            "last_class_crossed_nb"
        )


class EthnicitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ethnicities
        fields = "__all__"


class DialectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialects
        fields = "__all__"


class MemberExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Experiences
        fields = (
            "id",
            "member_nb",
            "position_nb",
            "start_date",
            "end_date",
            "chapter_nb",
        )


class MembersSerializerFull(serializers.ModelSerializer):
    # chapter_nb = ChapterSerializer(many=False, read_only=True)
    experiences = MemberExperiencesSerializer(many=True, read_only=True)
    ethnicity_txt = EthnicitiesSerializer(many=True, read_only=True)
    dialects_txt = DialectsSerializer(many=True, read_only=True)
    # StringRelatedField calls the __str__ method on the corresponding model
    # i.e., Chapter_nb is a FK to Chapter
    # chapter_nb = serializers.StringRelatedField(many=False)

    class Meta:
        model = Member
        fields = [
            "id",
            "first_name_txt",
            "last_name_txt",
            "ethnicity_txt",
            "dialects_txt",
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


class MembersSerializerAbbr(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "first_name_txt",
            "last_name_txt",
            "nickname_txt",
            "chapter_nb",
            "crossing_chapter_nb",
            "crossing_class_txt",
            "crossing_date",
            "line_nb",
            "big_nb",
            "tree_txt",
            "status_txt",
            "email_address_txt",
        ]


class ChapterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    chapter_stats = serializers.SerializerMethodField()
    members = MembersSerializerFull(many=True, read_only=True)

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
            "org_website_txt",
            "school_website_txt",
            "members",
        )

    def get_chapter_stats(self, obj):
        active_nb = 0
        inactive_nb = 0
        alumni_nb = 0
        memorial_nb = 0
        total_crossed_nb = 0
        class_counts = {}
        smallest_class_crossed_nb = float('inf')
        largest_class_crossed_nb = float('-inf')
        
        members = Member.objects.filter(
            Q(chapter_nb=obj) | Q(crossing_chapter_nb=obj)
    )

        for member in members:
            status = member.status_txt
            crossing_class = member.crossing_class_txt

            if member.chapter_nb == obj:
                if status == "AC":
                    active_nb += 1
                elif status in ["IM", "IN", "PI"]:
                    inactive_nb += 1
                elif status == "AL":
                    alumni_nb += 1
                elif status == "ME":
                    memorial_nb += 1
            
            if member.crossing_chapter_nb == obj or member.crossing_chapter_nb == None:
                total_crossed_nb += 1
                if crossing_class in class_counts:
                    class_counts[crossing_class] += 1
                else:
                    class_counts[crossing_class] = 1
                if crossing_class:
                    smallest_class_crossed_nb = min(smallest_class_crossed_nb, class_counts[crossing_class])
                    largest_class_crossed_nb = max(largest_class_crossed_nb, class_counts[crossing_class])

            average_class_crossed_fl = (
                sum(class_counts.values()) / len(class_counts)
            ) if class_counts else None

        chapter_stats = Chapter_Stats(
            active_nb=active_nb,
            inactive_nb=inactive_nb,
            alumni_nb=alumni_nb,
            memorial_nb=memorial_nb,
            total_crossed_nb=total_crossed_nb,
            smallest_class_crossed_nb=smallest_class_crossed_nb if smallest_class_crossed_nb != float('inf') else None,
            largest_class_crossed_nb=largest_class_crossed_nb if largest_class_crossed_nb != float('-inf') else None,
            average_class_crossed_fl=average_class_crossed_fl,
            last_class_crossed_nb=max(class_counts.keys(), key=int, default=None),
        )

        serializer = ChapterStatsSerializer(chapter_stats)

        return serializer.data


class PositionsTitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position_Titles
        fields = "__all__"


class ExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ("email", "first_name", "last_name", "member_nb")

    member_nb = MembersSerializerFull(many=False, read_only=True)


class JobOppsAndReferralsSerializer(serializers.ModelSerializer):
    poster_nb = MembersSerializerAbbr(many=False, read_only=True)
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
        fields = "__all__"


class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = "__all__"


class CurrentPESerializer(serializers.ModelSerializer):
    process_educator = serializers.SerializerMethodField()

    class Meta:
        model = Member_Experiences
        fields = (
            # "chapter_nb",
            "start_date",
            "end_date",
            "id",
            "process_educator",
        )

    def get_process_educator(self, member_experience):
        # Retrieve the Member instance for the current Member_Experiences object
        member = member_experience.member_nb

        # Return the member_id of the process educator
        return MembersSerializerAbbr(member).data