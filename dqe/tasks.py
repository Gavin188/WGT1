# from __future__ import absolute_import, unicode_literals
# import datetime
# from celery import shared_task
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.core.mail import EmailMultiAlternatives
# from WGT1.celery import app
# from dqe.models import Inventory, ResetHistory
# from system.mixin import LoginRequiredMixin
# from django.views.generic.base import View
# from django.http import HttpResponse
# from datetime import datetime
# from django.core.serializers.json import DjangoJSONEncoder
# import json
# from django.db.models import Count
# from math import floor
# from django.db.models import F
# from system.models import UserProfile, Structure
# from datetime import datetime, timedelta
# from django.template import Context, loader
#
# class OvertimeDetect(LoginRequiredMixin, View):
#
#     # 点击 机台状态查询 > 已超时 按钮 的操作
#     def post(self, request):
#         res = dict()
#
#         # 点击reset(超时按钮)的情况:  思路 : 记录 哪个部门 哪个人 哪个时间 按了reset  >  按了reset之后 库存中的resetflag 变为true >
#         # > resetflag情况，定时器执行程序，(系统时间-机台当前入库时间 / 7 +1) * 7 + 机台当前入库时间, 发邮件 ，将resetflag 变为0
#
#         invObj = Inventory.objects.filter(id=request.POST.get("id"))  # 获取点击超时的机台
#
#         # 实例化ResetHistory
#         rh = ResetHistory()
#         rh.fk_inv = invObj[0]
#         rh.resetUser = request.user.username
#         rh.resetDept = request.user.department
#         # rh.resetTime =  #系统时间
#         # 备注：PM部门的张三2018-7-6进行了reset操作 #datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         rh.resetRemark = str(rh.resetDept) + "部門的" + str(rh.resetUser) + "在" + datetime.now().strftime(
#             "%Y-%m-%d %H:%M:%S") + "進行了RESET操作"
#
#         rh.save()
#
#         # Inventory 中的resetFlag = True
#         invObj[0].resetFlag = 1
#         invObj[0].save()
#
#         res['invObj'] = list(invObj.values(*['rel']))  # 注意： 此处不能传递一个对象，而应该是一个列表
#
#         res['result'] = True
#
#         return HttpResponse(json.dumps(res), content_type='application/json')
#
#
# # 全局变量 : 用于实现每天发一封邮件
# sendEmailDateTemp = 0
#
#
# @shared_task
# def overtimeDetect():
#     # celery -A UCS beat -l info
#
#     # 1. 不考虑reset的情况 > 思路：每小时执行overtimeDetect > 遍历整个库存表 > 得出此次超时的机台 > 根据部门分别发送相应的邮件到预定部门
#     # 2. 考虑机台借入时间间隔<1天的情况，因为间隔短，每天也可能发多封邮件 > 那么第二封邮件不包含上一封邮件机台的信息 >
#     # 解决方式：定时器设定一天工作一次，那么一天清算一次，一天就发一封邮件了。
#
#     global sendEmailDateTemp  # 表示函数中使用全局变量
#
#     res = dict()
#     invObjs = Inventory.objects.filter(resetFlag=0)
#
#     # 1. 思路 ： # 判断机台是否超过了该部门预设的延迟时间 > 如果有 > 将机台保存到该部门列表下  > 循环结束后相应的发邮件
#
#     for invObj in invObjs:
#
#         # 当前停留时长 = 系统时间 - 机台入库当前接收时间
#         stayTime = datetime.now() - datetime.strptime(invObj.currRecDate, '%Y-%m-%d %H:%M:%S.%f')
#         # 得出部门设定reset时长 3种情况   D    H    D H    将resetTime 进行切割
#         deptReset = invObj.fk_structure.resetTime.split(' ')
#
#         # 存储相应的部门 下 相应的超时机台信息
#         if len(deptReset) == 1:  # 判断用户设定reset的形式
#             if deptReset[0][1] == 'D':
#                 if int(stayTime.days) >= int(deptReset[0][0]):  # 说明该机台应存储到相应部门，然后在以邮件形式发送
#                     if invObj.fk_structure.name in res:  # 判断部门key在res中 目的：将该部门超时的机台汇总
#                         res[invObj.fk_structure.name].append(invObj.id)
#                     else:
#                         res[invObj.fk_structure.name] = []
#                         res[invObj.fk_structure.name].append(invObj.id)
#                 else:
#                     pass  # 如果机台不超时则不进行任何操作
#
#             elif deptReset[0][1] == 'H':
#                 if int(floor(stayTime.seconds / 60 / 60)) >= int(deptReset[0][0]):  # 说明该机台 应存储到相应部门，然后在以邮件形式发送
#                     if invObj.fk_structure.name in res:  # 判断部门key在res中 目的：将该部门超时的机台汇总
#                         res[invObj.fk_structure.name].append(invObj.id)
#                     else:
#                         res[invObj.fk_structure.name] = []
#                         res[invObj.fk_structure.name].append(invObj.id)
#                 else:
#                     pass  # 如果机台不超时则不进行任何操作
#
#             else:
#                 pass  # reset设定 D 或者 H 的情况结束
#
#         elif len(deptReset) == 2:
#
#             if deptReset[0][1] == 'D' and deptReset[1][1] == 'H':
#                 if int(stayTime.days) >= int(deptReset[0][0]) and int(floor(stayTime.seconds / 60 / 60)) >= int(
#                         deptReset[1][0]):  # 说明该机台应存储到相应部门，然后在以邮件形式发送
#                     if invObj.fk_structure.name in res:  # 判断部门key在res中 目的：将该部门超时的机台汇总
#                         res[invObj.fk_structure.name].append(invObj.id)
#                     else:
#                         res[invObj.fk_structure.name] = []
#                         res[invObj.fk_structure.name].append(invObj.id)
#                 else:
#                     pass  # 如果机台不超时则不进行任何操作
#
#         else:
#             pass  # 出现这种情况 只能说设定异常了
#
#     # 2. 各部门机台超时的信息已经集结完毕 > 如何控制一天内只发一封邮件 > 解决方式： 这里考虑定时器每隔一小时执行一次的情况
#
#     # 思路： 判断是否有超时机台 > 得到发邮件的日期 > 判断该日期是否与sendEmailDateTemp日期相同 > 如果等于则不发，反之则发邮件 >
#
#     fields = ['id', 'fk_project__pname', 'fk_stage__sname', 'rel', 'sn', 'indate', 'recuser', 'state',
#               'fk_structure__name', 'remark', 'currRecUser', 'currRecDate', 'fk_pt__ptname',
#               'fk_structure__resetTime']
#
#     if len(res):  # 如果res不为空，那么就有相应的部门有超时机台
#         # 发邮件日期 = 当前系统时间日期
#         sysDate = datetime.strptime(datetime.now().strftime("%Y-%m-%d"),
#                                     '%Y-%m-%d')  # datetime.now().strftime("%Y-%m-%d %H:%M:%S") 字符串
#         if sendEmailDateTemp == sysDate:
#             pass
#         else:
#             sendEmailDateTemp = sysDate  # 将今天日期 赋予 缓存日期
#             # 循环遍历 res  >  将key(部门)所对应的邮箱全部遍历出来[列表形式] > 将所有value的信息查询出来(根据id查询Inventory)，当做邮件的内容
#             for key, value in res.items():
#                 # 获取邮箱信息列表
#                 # sendEmailUsers = UserProfile.objects.filter(department=Structure.objects.get(name=key)).values(
#                 #     'email')  # ,'department__name'
#                 # seuslist = [i['email'] for i in sendEmailUsers]
#                 seuslist = Structure.objects.get(name=key).sendUserEmail.replace('，', ',').split(',')
#                 # 获取要发邮箱的信息
#                 # sendEmailInfo = str(list(Inventory.objects.filter(id__in=value).values(*['rel', 'sn', ])))
#                 sendEmailInfo = list(Inventory.objects.filter(id__in=value).values(*['fk_project__pname', 'fk_stage__sname', 'fk_structure__name', 'rel', 'sn', ]))
#
#                 # 發送郵件
#                 #     # 值1： 邮件标题     值2： 邮件主体
#                 #     # 值3： 发件人       值4： 收件人             # 注意 send_mail str(sendEmailInfo)
#                 # send_mail('UCS機台流向追溯系統--機台超時郵件提示', '超时编号和SN如下' + sendEmailInfo, 'UCS@mail.foxconn.com', seuslist, )
#
#                 subject, from_email, to = 'UCS機台流向追溯系統--機台超時郵件提示', 'UCS@mail.foxconn.com', [
#                     'forest.jl.song@foxconn.com', ]
#                 email_template_name = 'email_info.html'
#
#                 t = loader.get_template(email_template_name)
#                 html_content = t.render({'data': sendEmailInfo})  # Context(sendEmailInfo)
#
#                 msg = EmailMultiAlternatives(subject, html_content, from_email, to)
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()
#
#         resetRes = dict()
#
#         # 以上是无点击reset的情况，接下来是点击reset的情况 (点 已超时)
#         resetInvObjs = Inventory.objects.filter(resetFlag=1)
#
#         # 计算出下一次发邮件的日期 > 发邮件之后，将Inventory中的resetFlag变为0。
#         for resetInvObj in resetInvObjs:
#             # 判断这些机台中是否有 系统时间(精确到分钟) > 发邮件日期 =（（系统时间 - 当前入库时间） %  reset时长  +  1  ） * reset时长 + 当前入库时间
#
#             # datetime.now() + timedelta(days=-7)
#             # currRecDate = datetime.strptime(resetInvObj.currRecDate, '%Y-%m-%d %H:%M:%S.%f')  当前入库时间
#             # timeInterval = datetime.now() - datetime.strptime(resetInvObj.currRecDate, '%Y-%m-%d %H:%M:%S.%f') = （系统时间 - 当前入库时间）
#             # intervalDays = (((timeInterval.days + timeInterval.seconds/60/60/24) / int(deptReset[0][0])) +1)  * int(deptReset[0][0])
#             # sendEmailDateReset = currRecDate + timedelta(days=intervalDays)
#
#             deptReset = resetInvObj.fk_structure.resetTime.split(' ')
#
#             if len(deptReset) == 1:  # 判断用户设定reset的形式
#                 if deptReset[0][1] == 'D':
#                     resetTimer = int(deptReset[0][0])
#                 elif deptReset[0][1] == 'H':
#                     resetTimer = int(deptReset[0][0]) / 24  # 得到天
#             elif len(deptReset) == 2:
#                 resetTimer = int(deptReset[0][0]) + int(deptReset[1][0]) / 24
#
#             currRecDate = datetime.strptime(resetInvObj.currRecDate, '%Y-%m-%d %H:%M:%S.%f')  # 当前入库时间 得到对象
#             timeInterval = datetime.now() - datetime.strptime(resetInvObj.currRecDate,
#                                                               '%Y-%m-%d %H:%M:%S.%f')  # 得到机台停留时长间隔
#             intervalDays = int(
#                 ((timeInterval.days + timeInterval.seconds / 60 / 60 / 24) / resetTimer) + 1) * resetTimer  # 得到间隔的天数
#             sendEmailDateReset = currRecDate + timedelta(days=intervalDays)  # 得到发邮件的日期
#
#             if datetime.now() > sendEmailDateReset:
#                 if resetInvObj.fk_structure.name in resetRes:  # 判断部门key在res中 目的：将该部门超时的机台汇总
#                     resetRes[resetInvObj.fk_structure.name].append(resetInvObj.id)
#                 else:
#                     resetRes[resetInvObj.fk_structure.name] = []
#                     resetRes[resetInvObj.fk_structure.name].append(resetInvObj.id)
#
#         # 数据收集完毕
#         if len(resetRes):  # 如果res不为空，说明已经过了reset设定的两倍时间
#             # 循环遍历 res  >  将key(部门)所对应的邮箱全部遍历出来[列表形式] > 将所有value的信息查询出来(根据id查询Inventory)，当做邮件的内容
#             for key, value in resetRes.items():
#                 seuslist = Structure.objects.get(name=key).sendUserEmail.replace('，', ',').split(',')
#                 # 获取要发邮箱的信息
#                 #sendEmailInfo = str(list(Inventory.objects.filter(id__in=value).values(*['rel', 'sn', ])))
#
#                 sendEmailInfo = list(Inventory.objects.filter(id__in=value).values(*['fk_project__pname', 'fk_stage__sname', 'fk_structure__name', 'rel', 'sn', ]))
#
#                 Inventory.objects.filter(id__in=value).update(resetFlag=0)
#
#                 # 發送郵件
#                 #     # 值1： 邮件标题     值2： 邮件主体
#                 #     # 值3： 发件人       值4： 收件人
#                 # send_mail('UCS機台流向追溯系統--機台超時郵件提示',
#                 #           '超时编号和SN如下' + sendEmailInfo,
#                 #           'UCS@mail.foxconn.com',
#                 #           seuslist, )
#
#                 subject, from_email, to = 'UCS機台流向追溯系統--RESET機台超時郵件提示', 'UCS@mail.foxconn.com', [
#                     'forest.jl.song@foxconn.com', ]
#                 email_template_name = 'email_info.html'
#
#                 t = loader.get_template(email_template_name)
#                 html_content = t.render({'data': sendEmailInfo})  # Context(sendEmailInfo)
#
#                 msg = EmailMultiAlternatives(subject, html_content, from_email, to)
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()
#
# # @app.task(bind=True)
# # def testTimer(self):
# #     print('测试定时器')
#
# ''' redis程序
# from __future__ import absolute_import
# from UCS.celery import app
# @app.task()
# def interval_task():
#     # celery -A UCS worker -l info --beat 啟動定時任務
#     print("我每隔5秒钟时间执行一次....")
# '''
