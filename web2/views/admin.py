from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from web2 import models
from web2.urls.form import AdminModelForm


def admin_list(request):
    """管理员列表"""
    # 搜索,参数q
    query_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        query_dict['username__contains'] = search_data
    queryset = models.Admin.objects.filter(**query_dict)

    # 分页
    page_num = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    c_page = paginator.page(int(page_num))

    return render(request, 'admin_list.html', locals())


def admin_add(request):
    """添加管理员"""
    title = '添加管理员'
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', locals())

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', locals())
