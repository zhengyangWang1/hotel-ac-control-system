from django.db import models

# Create your models here.
class Manager(models.Model):
    # manager_id = models.AutoField('manager_id', primary_key=True)
    manager_type = models.CharField('manager_type', max_length=30)
    manager_name = models.CharField('manager_name', max_length=10,primary_key=True)
    # 密码
    password = models.CharField('password', max_length=30)
    # 指定表名
    class Meta:
        db_table = 'Manager'