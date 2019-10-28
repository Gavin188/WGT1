import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from system.models import TestWord


class WordView(View):
    '''测试说明书 视图'''

    def get(self, request):
        return render(request, 'system/Test_Word/WordList.html')


class WordListView(View):
    '''测试说明书列表'''

    def get(self, request):
        res = {}
        fields = ['id', 'title', 'comments', 'publisher', 'publish_date']
        #
        searchFields = ['publish_date']  # 与数据库字段一致

        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}
        print(filters)
        all_obj = list(TestWord.objects.filter(**filters).values(*fields).order_by('-publish_date'))
        res['data'] = all_obj

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class WordUpdateView(View):
    ''' 测试说明书 新建 和 更新'''

    def get(self, request):
        return render(request, 'system/Test_Word/UpdateWord.html')

    def post(self, request):
        res = dict(result='创建失败')
        title = request.POST.get('title')
        publisher = request.POST.get('publisher')
        comments = request.POST.get('comments')
        editor = request.POST.get('editor')

        data = [i['title'] for i in list(TestWord.objects.filter().values('title'))]
        print(data)

        if title == '':
            res['result'] = '创建失败，标题不能为空！！！'
        elif title in data:
            res['result'] = '创建失败，标题已经存在'
        else:
            try:
                test_word = TestWord()
                test_word.title = title
                test_word.publisher = publisher
                test_word.comments = comments
                test_word.desc_pack = editor
                test_word.save()
                res['result'] = '创建成功'
            except Exception:
                res['result'] = '未知错误'

        return HttpResponse(res.values(), content_type='application/json')


class WordDetailView(View):
    '''显示 创建的测试word内容'''

    def get(self, request):
        fields = ['id', 'title', 'publisher', 'comments', 'desc_pack']
        all_obj = []
        print(request.GET)
        if 'id' in request.GET and request.GET['id']:
            word_id = request.GET.get('id')
            all_obj = list(TestWord.objects.filter(id=word_id).values(*fields))
        elif 'title' in request.GET and request.GET['title']:
            print(1111)
            title = request.GET.get('title')
            all_obj = list(TestWord.objects.filter(title=title).values(*fields))
        print(all_obj)

        return render(request, 'system/Test_Word/DetailWord.html', {'all': all_obj})


class WordDeleteView(View):
    '''删除 测试word 文档'''

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            TestWord.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')
