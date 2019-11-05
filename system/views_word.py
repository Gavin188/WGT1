import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views import View

from system.forms import UEditorTestModelForm
from system.models import TestWord


class WordView(View):
    '''测试说明书 视图'''

    def get(self, request):
        return render(request, 'system/Test_Word/WordList.html')


class WordListView(View):
    '''测试说明书列表'''

    def get(self, request):
        res = {}
        fields = ['id', 'title', 'publisher', 'publish_date']
        #
        searchFields = ['publish_date']  # 与数据库字段一致

        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}
        # print(filters)
        all_obj = list(TestWord.objects.filter(**filters).values(*fields).order_by('-publish_date'))
        res['data'] = all_obj

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class WordUpdateView(View):
    ''' 测试说明书 新建 和 更新'''

    def get(self, request):
        # title = request.GET.get('title')
        # title = list(CaseRegister.objects.filter(id=id).values('desc'))[0]['desc']

        form = UEditorTestModelForm(
            initial={'Description': '请输入：'}
        )
        context = {
            # 'title': title,
            'form': form,
        }
        return render(request, 'system/Test_Word/UpdateWord.html', context)

    def post(self, request):
        # res = dict(result='创建失败')
        # print(request.POST)
        form = UEditorTestModelForm(request.POST)
        if form.is_valid():
            form.save()
            # print('OK')
            return HttpResponse(u"上传成功！")
        else:
            return HttpResponse(u"数据校验错误")

        # return HttpResponse(res.values(), content_type='application/json')


class WordDetailView(View):
    '''显示 创建的测试word内容'''

    def get(self, request):
        fields = ['id', 'title', 'publisher', 'desc_pack']
        all_obj = []
        # 测试说明 id 查询
        if 'id' in request.GET and request.GET['id']:
            word_id = request.GET.get('id')
            all_obj = list(TestWord.objects.filter(id=word_id).values(*fields))
        # 今日测试 中 标题查询
        elif 'title' in request.GET and request.GET['title']:
            title = request.GET.get('title')
            print(title)
            all_obj = list(TestWord.objects.filter(title=title).values(*fields))

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
