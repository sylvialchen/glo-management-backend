# Generated by Django 4.1.5 on 2023-08-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0014_remove_chapter_inactive_chapter_fg"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chapter",
            options={
                "ordering": [
                    "chapter_status_txt",
                    "associate_chapter_fg",
                    "greek_letter_assigned_txt",
                    "original_founding_date",
                ]
            },
        ),
        migrations.AlterField(
            model_name="chapter",
            name="greek_letter_assigned_txt",
            field=models.CharField(max_length=50, null=True),
        ),
    ]