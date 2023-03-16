from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from web2 import models
from web2.urls.form import UserModelForm, PrettyModelForm, PrettyEditModelForm




def user_list(request):
    """用户管理"""

    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {'queryset': queryset})


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