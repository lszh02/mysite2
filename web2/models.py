from django.db import models


class Department(models.Model):
    """部门表"""
    def __str__(self):
        return self.title
    # id = models.BigAutoField(verbose_name='id',primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=32)


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    salary = models.DecimalField(verbose_name='薪资', max_digits=18, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')
    # Django中的约束
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    # 部门需要外键约束
    # to 关联的表
    # to_field 关联的字段
    # on_delete 级联删除
    depart = models.ForeignKey(verbose_name='部门 ', to='Department', to_field='id', on_delete=models.CASCADE)
    # 置空
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)
