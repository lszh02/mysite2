from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from web2 import models
from web2.urls.form import AdminModelForm, AdminEditModelForm


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


def admin_edit(request, nid):
    """编辑管理员"""
    # row_obj得到对象或None
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        error_msg = '数据不存在'
        return render(request, 'error.html', locals())
        # return redirect('/admin/list/')

    title = '编辑管理员'

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_obj)
        return render(request, 'change.html', locals())

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', locals())


def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')
