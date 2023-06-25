from django.db import models


# Create your models here.

# レース情報
class RaceInfo(models.Model):
    race_id = models.CharField(
        primary_key=True,
        max_length=50,
        blank=False,
        null=False,
        unique=False,
        verbose_name='レースID',
    )

    race_date = models.DateField(
        blank=False,
        null=False,
        verbose_name='日付',
    )

    start_time = models.TimeField(
        blank=False,
        null=False,
        verbose_name='発走時刻',
    )

    distance = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='距離(m)',
    )

    direction = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='方向(右or左)',
    )

    ground_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='地面種類',
    )

    ground_condition = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='地面状態',
    )

    weather = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='天候',
    )

    race_cource = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='競馬場',
    )

    entries = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='頭数',
    )

    update_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name='更新日時',
    )

    delete_flag = models.IntegerField(
        default=0,
        verbose_name='削除フラグ',
    )

    def __str__(self):
        return self.race


class RaceResult(models.Model):

    race = models.ForeignKey(
        'RaceInfo',
        on_delete=models.CASCADE,
    )

    horse_id = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='馬ID',
    )

    horse_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='馬名',
    )

    order = models.CharField(
        blank=False,
        null=False,
        verbose_name='着順',
    )

    bracket_number = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='枠番',
    )

    sexual_age = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='性齢',
    )

    weight = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='斤量',
    )

    time = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='タイム',
    )

    horse_weight = models.CharField(
        blank=False,
        null=False,
        verbose_name='馬体重',
    )

    update_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name='更新日時',
    )

    delete_flag = models.IntegerField(
        default=0,
        verbose_name='削除フラグ',
    )

    def __str__(self):
        return self.race
