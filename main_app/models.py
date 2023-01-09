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

NICKNAME_STATUS = (
    ("RE", "Requested"),
    ("AP", "Approved"),
    ("QU", "Queued"),
    ("DE", "Denied")
)

GREEK_CLASS = (('01', "Alpha"), ('02', "Beta"), ('03', "Gamma"), ('04', "Delta"), ('05', "Epsilon"), ('06', "Zeta"), ('07', "Eta"), ('08', "Theta"), ('09', "Iota"), (10, "Lambda"),
               (11, "Mu"), (12, "Nu"), (13, "Xi"), (14, "Omicron"), (15, "Pi"), (16, "Rho"), (17, "Sigma"), (18, "Tau"), (19, "Upsilon"), (20, "Phi"), (21, "Chi"), (22, "Psi"), (23, "Omega"))


class Chapter(models.Model):
    name = models.CharField(max_length=50)
    chapter_school = models.CharField(max_length=50)
    city_state = models.CharField(max_length=50)
    original_founding_date = models.DateField()
    recharter_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('chapter_detail', kwargs={'chapter_id': self.id})

    def __str__(self):
        return f"{self.name} @ {self.chapter_school}"


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
    crossing_semester = models.CharField(max_length=6)
    crossing_year = models.IntegerField()
    big_sister = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    tree = models.CharField(max_length=20)
    line_number = models.IntegerField(null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=STATUS[0][0])

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
