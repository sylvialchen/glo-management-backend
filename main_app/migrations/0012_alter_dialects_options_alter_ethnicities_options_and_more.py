# Generated by Django 4.1.5 on 2023-04-18 14:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0011_dialects_ethnicities_alter_member_big_nb_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dialects",
            options={"ordering": ["dialect_txt"]},
        ),
        migrations.AlterModelOptions(
            name="ethnicities",
            options={"ordering": ["ethnicity_txt"]},
        ),
        migrations.AlterModelOptions(
            name="member_experiences",
            options={"ordering": ["-end_date"]},
        ),
    ]
