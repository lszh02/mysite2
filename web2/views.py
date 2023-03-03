from django import forms
from django.shortcuts import render, redirect

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
        return render(request, 'user_list.html', {'form': form})

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {'form': form})
