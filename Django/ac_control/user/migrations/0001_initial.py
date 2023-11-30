# Generated by Django 3.2.22 on 2023-11-30 05:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False, verbose_name='operation_id')),
                ('request_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='请求发出时间')),
                ('room_id', models.CharField(max_length=10, verbose_name='room_id')),
                ('user_id', models.CharField(max_length=30, verbose_name='user_id')),
                ('init_temp', models.IntegerField(default=0.0, verbose_name='初始温度')),
                ('current_temp', models.IntegerField(default=25.0, verbose_name='当前温度')),
                ('target_temp', models.IntegerField(default=0.0, verbose_name='目标温度')),
                ('fan_speed', models.IntegerField(choices=[(3, 'HIGH'), (2, 'MIDDLE'), (1, 'LOW')], default=2, verbose_name='风速')),
                ('state', models.IntegerField(choices=[(1, 'SERVING'), (2, 'WAITING'), (3, 'SHUTDOWN'), (4, 'BACKING')], default=3, verbose_name='服务状态')),
                ('serve_time', models.IntegerField(default=0, verbose_name='当前服务时长')),
                ('wait_time', models.IntegerField(default=0, verbose_name='当前等待时长')),
                ('operation', models.IntegerField(choices=[(1, '调温'), (2, '调风'), (3, '开机'), (4, '关机')], default=0, verbose_name='操作类型')),
                ('scheduling_num', models.IntegerField(default=0, verbose_name='调度次数')),
                ('fee', models.FloatField(default=0.0, verbose_name='费用')),
            ],
            options={
                'db_table': 'Room',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='user_id')),
                ('room_id', models.CharField(max_length=10, verbose_name='room_id')),
                ('password', models.CharField(max_length=30, verbose_name='password')),
                ('begin_date', models.DateField(auto_now=True, max_length=30, verbose_name='begin_date')),
                ('out_date', models.DateTimeField(auto_now=True, max_length=30, verbose_name='out_date')),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
