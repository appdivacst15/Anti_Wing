# Generated by Django 4.2.1 on 2023-06-25 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RaceInfo",
            fields=[
                (
                    "race_id",
                    models.CharField(
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                        verbose_name="レースID",
                    ),
                ),
                ("race_date", models.DateField(verbose_name="日付")),
                ("start_time", models.TimeField(verbose_name="発走時刻")),
                ("distance", models.IntegerField(verbose_name="距離(m)")),
                ("direction", models.CharField(max_length=50, verbose_name="方向(右or左)")),
                ("ground_type", models.CharField(max_length=50, verbose_name="地面種類")),
                (
                    "ground_condition",
                    models.CharField(max_length=50, verbose_name="地面状態"),
                ),
                ("weather", models.CharField(max_length=50, verbose_name="天候")),
                ("race_cource", models.CharField(max_length=50, verbose_name="競馬場")),
                ("entries", models.IntegerField(verbose_name="頭数")),
                (
                    "update_datetime",
                    models.DateTimeField(auto_now=True, verbose_name="更新日時"),
                ),
                ("delete_flag", models.IntegerField(default=0, verbose_name="削除フラグ")),
            ],
        ),
        migrations.CreateModel(
            name="RaceResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("horse_id", models.CharField(max_length=50, verbose_name="馬ID")),
                ("horse_name", models.CharField(max_length=50, verbose_name="馬名")),
                ("order", models.CharField(verbose_name="着順")),
                ("bracket_number", models.IntegerField(verbose_name="枠番")),
                ("sexual_age", models.CharField(max_length=50, verbose_name="性齢")),
                ("weight", models.IntegerField(verbose_name="斤量")),
                (
                    "time",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="タイム"
                    ),
                ),
                ("horse_weight", models.CharField(verbose_name="馬体重")),
                (
                    "update_datetime",
                    models.DateTimeField(auto_now=True, verbose_name="更新日時"),
                ),
                ("delete_flag", models.IntegerField(default=0, verbose_name="削除フラグ")),
                (
                    "race",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scraping.raceinfo",
                    ),
                ),
            ],
        ),
    ]
