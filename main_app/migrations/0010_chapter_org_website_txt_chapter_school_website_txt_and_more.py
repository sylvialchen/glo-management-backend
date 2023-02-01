# Generated by Django 4.1.5 on 2023-01-26 16:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0009_position_titles_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chapter",
            name="org_website_txt",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="chapter",
            name="school_website_txt",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="job_opps_and_referrals",
            name="pub_date",
            field=models.DateTimeField(
                auto_created=True,
                default=django.utils.timezone.now,
                verbose_name="date published",
            ),
        ),
        migrations.AlterField(
            model_name="nickname_request",
            name="req_date",
            field=models.DateTimeField(
                auto_created=True,
                default=django.utils.timezone.now,
                verbose_name="date requested",
            ),
        ),
    ]