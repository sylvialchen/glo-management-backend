# Generated by Django 4.1.5 on 2023-01-10 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0005_remove_chapter_name_chapter_associate_chapter_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chapter",
            name="chapter_status",
            field=models.CharField(
                choices=[("AC", "Active"), ("IN", "Inactive")],
                default="AC",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="chapter",
            name="greek_letter_assigned",
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name="job_opps_and_referrals",
            name="pub_date",
            field=models.DateTimeField(
                auto_created=True,
                default=datetime.datetime(
                    2023, 1, 10, 19, 57, 25, 272463, tzinfo=datetime.timezone.utc
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
                    2023, 1, 10, 19, 57, 25, 272134, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date requested",
            ),
        ),
        migrations.AlterField(
            model_name="sister",
            name="email_address",
            field=models.EmailField(max_length=30, null=True),
        ),
    ]
