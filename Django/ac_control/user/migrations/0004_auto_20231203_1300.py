# Generated by Django 3.2.22 on 2023-12-03 05:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20231202_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='request_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 5, 0, 4, 327796, tzinfo=utc), verbose_name='请求发出时间'),
        ),
        migrations.AlterField(
            model_name='room',
            name='sever_begin_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 5, 0, 4, 327796, tzinfo=utc), verbose_name='服务开始时间'),
        ),
        migrations.AlterField(
            model_name='room',
            name='sever_over_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 5, 0, 4, 327796, tzinfo=utc), verbose_name='服务结束时间'),
        ),
    ]
