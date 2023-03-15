from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from web2 import models


def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    title = request.POST.get('title')
    models.Department.objects.create(title=title)

    return redirect('/depart/list/')


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def depart_edit(request, nid):
    """修改部门"""
    if request.method == 'GET':
        row_obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_obj': row_obj})

    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')


def user_list(request):
    """用户管理"""

    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {'queryset': queryset})


class UserModelForm(forms.ModelForm):
    # name = forms.CharField(min_length=3, label="用户名")   重写字段，用于页面校验
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'salary', 'create_time', 'gender', 'depart']
        # widgets = {'name':forms.TextInput(attrs={'class':"form-control"})}
        # widgets = {'password': forms.PasswordInput(attrs={'class':"form-control"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "password":
                field.widget = forms.PasswordInput()
                # continue
            field.widget.attrs = {"class": "form-control"}


def user_add(request):
    """添加用户"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})

    # 获取用户POST提交的数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    """ 编辑用户"""
    # 根据id去数据库获取要编辑的那一行数据
    row_obj = models.UserInfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(request):
    """靓号列表"""
    query_dict = {}
    # 接收搜索参数q
    search_data = request.GET.get('q', '')
    if search_data:
        query_dict['mobile__contains'] = search_data

    queryset = models.PrettyNum.objects.filter(**query_dict).order_by('-level')

    # 分页
    page_num = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    c_page = paginator.page(int(page_num))
    return render(request, 'pretty_list.html', locals())


class PrettyModelForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "password":
                field.widget = forms.PasswordInput()
                # continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

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


def pretty_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


class PrettyEditModelForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "password":
                field.widget = forms.PasswordInput()
                # continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

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


def pretty_edit(request, nid):
    """编辑靓号"""
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).first().delete()
    return redirect('/pretty/list/')
