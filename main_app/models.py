from django.db import models
from django.urls import reverse
from django.utils import timezone
from authemail.models import EmailUserManager, EmailAbstractUser
from django.conf import settings
from main_app.model_choices import (
    STATUS,
    CHAPTER_STATUS,
    NICKNAME_STATUS,
    GREEK_CLASS,
    JOB_LEVEL,
    JOB_FAMILY,
    EVENT,
)


class Chapter(models.Model):
    associate_chapter_fg = models.BooleanField(default=True)
    greek_letter_assigned_txt = models.CharField(max_length=15, blank=False, null=True)
    chapter_school_txt = models.CharField(max_length=50)
    city_state_txt = models.CharField(max_length=50)
    original_founding_date = models.DateField()
    recharter_date = models.DateField(null=True, blank=True)
    chapter_status_txt = models.CharField(
        max_length=2, choices=CHAPTER_STATUS, default=CHAPTER_STATUS[0][0]
    )
    org_website_txt = models.CharField(max_length=50, null=True)
    school_website_txt = models.CharField(max_length=50, null=True)

    def __str__(self):
        if self.associate_chapter_fg:
            return f"Associate Chapter @ {self.chapter_school_txt}"
        return f"{self.greek_letter_assigned_txt} @ {self.chapter_school_txt}"

    class Meta:
        ordering = ["chapter_status_txt", "associate_chapter_fg", "greek_letter_assigned_txt", "original_founding_date"]


class Industry(models.Model):
    industry_txt = models.CharField(max_length=50)


class Ethnicities(models.Model):
    ethnicity_txt = models.CharField(max_length=50)

    class Meta:
        ordering = ["ethnicity_txt"]

    def __str__(self):
        return self.ethnicity_txt


class Dialects(models.Model):
    dialect_txt = models.CharField(max_length=50)

    class Meta:
        ordering = ["dialect_txt"]

    def __str__(self):
        return self.dialect_txt


class Member(models.Model):
    first_name_txt = models.CharField(max_length=20)
    last_name_txt = models.CharField(max_length=25)
    ethnicity_txt = models.ManyToManyField(Ethnicities)
    dialects_txt = models.ManyToManyField(Dialects)
    nickname_txt = models.CharField(max_length=20)
    nickname_meaning_txt = models.TextField(max_length=250)
    # DB_INDEX creates a B-Tree to quickly locate rows that match query conditions.
    # The B-Tree will automatically adjust itself each time data in these fields are modified/added/deleted.
    chapter_nb = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="active_chapter",
        db_index=True,
    )
    crossing_chapter_nb = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="crossing_chapter",
        db_index=True,
        blank=True,
        null=True,
    )
    crossing_class_txt = models.CharField(
        max_length=2,
        choices=GREEK_CLASS,
        default=None,
    )
    crossing_date = models.DateTimeField(
        "crossing date", auto_created=False, default=None
    )
    initiation_date = models.DateTimeField(
        "PNM initiation date", auto_created=False, default=None
    )
    line_nb = models.IntegerField(null=True)
    big_nb = models.ForeignKey("self", on_delete=models.PROTECT)
    tree_txt = models.CharField(max_length=20, blank=True, null=True)
    status_txt = models.CharField(max_length=2, choices=STATUS, default=STATUS[0][0])
    # current_address_txt = models.CharField(max_length=35, null=True)
    current_city_txt = models.CharField(max_length=30, null=True)
    current_state_txt = models.CharField(max_length=30, null=True)
    current_country_txt = models.CharField(max_length=15, null=True)
    email_address_txt = models.EmailField(max_length=30, null=True)
    coach_fg = models.BooleanField(default=False)
    current_position_txt = models.CharField(max_length=30, blank=True, null=True)
    current_company_txt = models.CharField(max_length=20, blank=True, null=True)
    linkedin_url_txt = models.CharField(max_length=50, blank=True, null=True)
    expertise_interests_nb = models.ForeignKey(
        Industry, on_delete=models.CASCADE, blank=True, null=True
    )
    summary_txt = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name_txt} {self.last_name_txt}, {self.nickname_txt}"

    # def get_absolute_url(self):
    #     return reverse('sister_detail', kwargs={'sister_id': self.id})


class MyUser(EmailAbstractUser):
    # Custom fields
    member_nb = models.OneToOneField(
        Member, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    # Required
    objects = EmailUserManager()


class Pnm(models.Model):
    first_name_txt = models.CharField(max_length=20)
    last_name_txt = models.CharField(max_length=25)
    process_chapter_nb = models.ForeignKey(
        Chapter,
        on_delete=models.PROTECT,
        related_name="process_chapter",
        blank=True,
        null=True,
    )
    # process_semester  = models.CharField(max_length=6)
    # process_year      = models.PositiveSmallIntegerField()
    # potential_line_nb = models.PositiveSmallIntegerField()
    big_nb = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"PNM {self.first_name_txt}"

    # def get_absolute_url(self):
    #     return reverse('pnm_detail', kwargs={'pnm_id': self.id})


class Nickname_Request(models.Model):
    name_txt = models.CharField("nickname request", max_length=20)
    nickname_meaning_txt = models.TextField(max_length=250)
    pnm_nb = models.ForeignKey(Pnm, on_delete=models.CASCADE, null=True)
    requestor_nb = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    req_date = models.DateTimeField(
        "date requested", auto_created=True, default=timezone.now
    )
    nickname_approval_status_txt = models.CharField(
        "Nickname Approval Status",
        max_length=2,
        choices=NICKNAME_STATUS,
        default=NICKNAME_STATUS[0][0],
    )

    def __str__(self):
        return f"PNM {self.name_txt}"

    # def get_absolute_url(self):
    #     return reverse('sister_detail', kwargs={'sister_id': self.id})

    #     class Meta:
    #         ordering = ['-date']


# class Nicknames(models.Model):
#     nickname_txt = models.CharField("nickname request", max_length=20)
#     nickname_meaning_txt = models.TextField(max_length=250)


class Job_Opps_And_Referrals(models.Model):
    pub_date = models.DateTimeField(
        "date published", auto_created=True, default=timezone.now
    )
    job_title_txt = models.CharField(max_length=50)
    company_name_txt = models.CharField(max_length=50)
    job_link_txt = models.CharField(max_length=250)
    remote_role_fg = models.BooleanField(default=False)
    city_txt = models.CharField(max_length=15, null=True)
    state_txt = models.CharField(max_length=15, null=True)
    level_of_opening_txt = models.CharField(
        max_length=2, choices=JOB_LEVEL, default=JOB_LEVEL[0][0]
    )
    industry_nb = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    description_txt = models.TextField(max_length=250)
    poster_nb = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.job_title_txt} @ {self.company_name_txt}"


class Position_Titles(models.Model):
    position_title_txt = models.CharField(max_length=50)
    active_fg = models.BooleanField(default=False)
    e_board_fg = models.BooleanField(default=False)
    description_txt = models.TextField(max_length=250)
    job_family_txt = models.CharField(
        max_length=2, choices=JOB_FAMILY, default=JOB_FAMILY[0][0]
    )

    def __str__(self):
        return f"{self.position_title_txt}, active: {self.active_fg} part of {self.job_family_txt} job family"


class Member_Experiences(models.Model):
    member_nb = models.ForeignKey(
        Member, related_name="experiences", on_delete=models.CASCADE, null=True
    )
    position_nb = models.ForeignKey(
        Position_Titles, on_delete=models.CASCADE, null=True
    )
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    chapter_nb = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.position_nb} from {self.start_date} to {self.end_date}"

    class Meta:
        ordering = ["-end_date"]


class Chapter_Stats(models.Model):
    active_nb = models.PositiveIntegerField()
    inactive_nb = models.PositiveIntegerField()
    alumni_nb = models.PositiveIntegerField()
    memorial_nb = models.PositiveIntegerField()
    total_crossed_nb = models.PositiveIntegerField()
    smallest_class_crossed_nb = models.PositiveIntegerField()
    largest_class_crossed_nb = models.PositiveIntegerField()
    average_class_crossed_fl = models.FloatField()

    # def __str__(self):
    #     return f"Active: {self.active_nb}, Inactive: {self.inactive_nb}, Alumni: {self.alumni_nb}, Deceased: {self.memorial_nb}, Total: {self.total_crossed_nb}"


class Events(models.Model):
    national_event = models.BooleanField(default=False)
    name = models.CharField(max_length=250)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50)
    url = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=2, choices=EVENT, null=True, blank=True)

    host_chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"National Event: {self.national_event}, Host: {self.host_chapter}, Name: {self.name}, Date: {self.date}, Location: {self.location}, URL: {self.url}, Description: {self.description}, Category: {self.category}"


class Announcements(models.Model):
    national_announcement_fg = models.BooleanField(default=True)
    chapter_announcement_nb = models.ForeignKey(
        Chapter, on_delete=models.SET_NULL, null=True, blank=True
    )
    # SEOs and SEO websites recommend a title tag length of approximately 50 to 70 characters because that’s what Google shows in their SERPs
    title_txt = models.CharField(max_length=60)
    # Twitter max character limit
    description_txt = models.CharField(max_length=280)
    link_txt = models.CharField(max_length=500, null=True, blank=True)
    start_posting_date = models.DateField(null=True, blank=True)
    end_posting_date = models.DateField(null=True, blank=True)
    request_date = models.DateTimeField(
        "date requested", auto_created=True, default=timezone.now
    )
    approved_fg = models.BooleanField(default=False)
