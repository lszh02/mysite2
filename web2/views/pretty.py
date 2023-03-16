from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from web2 import models
from web2.urls.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


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
