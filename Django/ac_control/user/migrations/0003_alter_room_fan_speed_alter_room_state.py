# Generated by Django 4.2.7 on 2023-12-07 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_room_fan_speed_alter_room_target_temp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='fan_speed',
            field=models.IntegerField(choices=[(3, '高'), (2, '中'), (1, '低')], default=2, verbose_name='风速'),
        ),
        migrations.AlterField(
            model_name='room',
            name='state',
            field=models.IntegerField(choices=[(1, '服务'), (2, '等待'), (3, '关机'), (4, '休眠')], default=3, verbose_name='服务状态'),
        ),
    ]
