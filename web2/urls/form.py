from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from web2 import models
from web2.urls.bootstrap import BootstrapModelForm
from web2.urls.encrypt import md5


class UserModelForm(BootstrapModelForm):
    # name = forms.CharField(min_length=3, label="用户名")   重写字段，用于页面校验
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'salary', 'create_time', 'gender', 'depart']


class PrettyModelForm(BootstrapModelForm):
    # 前端提交数据验证,方式一：字段+正则
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        fields = '__all__'
        # exclude = ['level']

    # 前端数据验证,方式二：钩子方法，clean_字段名
    def clean_mobile(self):
        # 获取用户输入的所有数据：cleaned_data
        input_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=input_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在！')
        # 验证不通过，前端报错
        if len(input_mobile) != 11:
            raise ValidationError('格式错误')
        # 验证通过,返回用户输入的数据
        return input_mobile


class PrettyEditModelForm(BootstrapModelForm):
    # 前端提交数据验证,方式一：字段+正则
    mobile = forms.CharField(
        disabled=True,
        label='手机号',
        # validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    # mobile = forms.CharField(disabled=True, label='手机号')  # 前端显示，但不可更改

    class Meta:
        model = models.PrettyNum
        fields = '__all__'
        exclude = ['level']

    # 前端数据验证,方式二：钩子方法，clean_字段名
    def clean_mobile(self):
        # 获取用户输入的数据
        input_mobile = self.cleaned_data['mobile']
        # 当前编辑的那一行的ID:self.instance.pk
        # exclude:排除自己这一条
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=input_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在！')
        # 验证不通过
        # if len(input_mobile) != 11:
        #     raise ValidationError('格式错误')
        # 验证通过
        return input_mobile


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(render_value=True)  # 密码输入错误时，保留输入
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError('密码不一致')
        return confirm


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']
