# Generated by Django 4.1.5 on 2023-01-10 20:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0006_chapter_chapter_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chapter",
            name="greek_letter_assigned",
        ),
        migrations.AlterField(
            model_name="job_opps_and_referrals",
            name="pub_date",
            field=models.DateTimeField(
                auto_created=True,
                default=datetime.datetime(
                    2023, 1, 10, 20, 4, 55, 826843, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date published",
            ),
        ),
        migrations.AlterField(
            model_name="nickname_request",
            name="req_date",
            field=models.DateTimeField(
                auto_created=True,
                default=datetime.datetime(
                    2023, 1, 10, 20, 4, 55, 826394, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date requested",
            ),
        ),
    ]
