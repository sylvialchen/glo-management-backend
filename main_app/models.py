from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# from datetime import date
import datetime
# from psycopg2 import Date

# Create your models here.

STATUS = (
    ("AC", "Active"),
    ("AL", "Alumnae"),
    ("DE", "Deceased"),
)

CHAPTER_STATUS = (
    ("AC", "Active"),
    ("IN", "Inactive"),
)

NICKNAME_STATUS = (
    ("RE", "Requested"),
    ("AP", "Approved"),
    ("QU", "Queued"),
    ("DE", "Denied")
)

GREEK_CLASS = (('01', "Alpha"), ('02', "Beta"), ('03', "Gamma"), ('04', "Delta"), ('05', "Epsilon"), ('06', "Zeta"), ('07', "Eta"), ('08', "Theta"), ('09', "Iota"), (10, "Lambda"),
               (11, "Mu"), (12, "Nu"), (13, "Xi"), (14, "Omicron"), (15, "Pi"), (16, "Rho"), (17, "Sigma"), (18, "Tau"), (19, "Upsilon"), (20, "Phi"), (21, "Chi"), (22, "Psi"), (23, "Omega"))

JOB_LEVEL = (
    ("00", "Internship"),
    ("01", "Entry"),
    ("02", "Associate"),
    ("03", "Analyst"),
    ("04", "Specialist"),
    ("05", "Manager"),
    ("06", "Senior Manager"),
    ("07", "Director"),
    ("08", "Senior Director"),
    ("09", "Executive"),
)


class Chapter(models.Model):
    associate_chapter = models.BooleanField(default=True)
    # greek_letter_assigned = (if associate_chapter == False:
    #                          models.CharField(
    #                              max_length=15, blank=False, null=False)
    #                          else models.CharField(max_length=1, null=True, blank=True))
    chapter_school = models.CharField(max_length=50)
    city_state = models.CharField(max_length=50)
    original_founding_date = models.DateField()
    recharter_date = models.DateField(null=True, blank=True)
    chapter_status = models.CharField(
        max_length=2, choices=CHAPTER_STATUS, default=CHAPTER_STATUS[0][0])

    def get_absolute_url(self):
        return reverse('chapter_detail', kwargs={'chapter_id': self.id})

    def __str__(self):
        return f"{self.name} @ {self.chapter_school}"


class Industry(models.Model):
    industry = models.CharField(max_length=50)


class Sister(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=25)
    nickname = models.CharField(max_length=20)
    nickname_meaning = models.TextField(max_length=250)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='active_chapter')
    crossing_chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='crossing_chapter', blank=True, null=True)
    crossing_class = models.CharField(
        max_length=2,
        choices=GREEK_CLASS,
        default=None,
    )
    crossing_date = models.DateTimeField(
        'crossing date', auto_created=False, default=None)
    initiation_date = models.DateTimeField(
        'PNM initiation date', auto_created=False, default=None)
    line_number = models.IntegerField(null=True)
    big_sister = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    tree = models.CharField(max_length=20)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=STATUS[0][0])
    current_city = models.CharField(max_length=15, null=True)
    current_state = models.CharField(max_length=15, null=True)
    current_country = models.CharField(max_length=15, null=True)
    email_address = models.EmailField(max_length=30, null=True)
    # User
    coach = models.BooleanField(default=False)
    current_position = models.CharField(max_length=30, null=True)
    current_company = models.CharField(max_length=20, null=True)
    linkedin_url = models.CharField(max_length=50, null=True)
    expertise_interests = models.ForeignKey(
        Industry, on_delete=models.DO_NOTHING, null=True)
    summary = models.TextField(max_length=250, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.nickname}"

    def get_absolute_url(self):
        return reverse('sister_detail', kwargs={'sister_id': self.id})


class Pnm(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=25)
    process_chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name='process_chapter', blank=True, null=True)
    process_semester = models.CharField(max_length=6)
    process_year = models.PositiveSmallIntegerField()
    potential_line_number = models.PositiveSmallIntegerField()
    big_sister = models.ForeignKey(
        Sister, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"PNM {self.first_name}"

    def get_absolute_url(self):
        return reverse('pnm_detail', kwargs={'pnm_id': self.id})


class Nickname_Request (models.Model):
    name = models.CharField("nickname request", max_length=20)
    nickname_meaning = models.TextField(max_length=250)
    pnm = models.ForeignKey(Pnm, on_delete=models.CASCADE, null=True)
    requestor = models.ForeignKey(Sister, on_delete=models.CASCADE, null=True)
    req_date = models.DateTimeField(
        'date requested', auto_created=True, default=timezone.now())
    nickname_approval_status = models.CharField("Nickname Approval Status",
                                                max_length=2,
                                                choices=NICKNAME_STATUS,
                                                default=NICKNAME_STATUS[0][0])
    # def was_requested_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.req_date <= now

    def __str__(self):
        return f"PNM {self.name}"

    def get_absolute_url(self):
        return reverse('sister_detail', kwargs={'sister_id': self.id})

    #     class Meta:
    #         ordering = ['-date']


class Job_Opps_And_Referrals(models.Model):
    pub_date = models.DateTimeField(
        'date published', auto_created=True, default=timezone.now())
    job_title = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    job_link = models.CharField(max_length=250)
    level_of_opening = models.CharField(max_length=2,
                                        choices=JOB_LEVEL,
                                        default=JOB_LEVEL[0][0])
    industry = models.ForeignKey(
        Industry, on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(max_length=250)
    poster = models.ForeignKey(Sister, on_delete=models.CASCADE, null=True)
