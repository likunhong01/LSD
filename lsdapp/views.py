from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum
from lsdapp import models
from django.db.models import Q

import requests
import random
import string
import hashlib


# Create your views here.
# 登录函数
def login(request):
    response = {}
    # if request.method == "GET":
    #     return render(request, 'login.html')
    if request.method == "POST":
        # 获取用户名
        name = request.POST.get("user_name")
        # 获取密码
        password = request.POST.get("password")
        # 尝试在用户表中查找此用户,若不存在则返回错误信息
        try:
            user = models.User.objects.get(user_name=name)
        except Exception :
            response['status'] = False
            return JsonResponse(data=response, safe=False)
        else:
            # 存在则进行密码匹配，取出随机字符串
            s = models.UserStr.objects.filter(user_name=name)
            # 创建MD5对象
            m = hashlib.md5()
            new_password = s+password+s
            b = new_password.encode(encoding='utf-8')
            m.update(b)
            new_password_md5 = m.hexdigest()
            # 如果密码正确进行身份判断，错误则返回错误信息
            if new_password_md5 == user.password:
                if user.authority == "boss":
                    requests.session['user_name'] = name
                    response['status'] = True
                    response['identity'] = 'boss'
                    return JsonResponse(data=response, safe=False)
                else:
                    requests.session['user_name'] = name
                    response['status'] = True
                    response['identity'] = 'salesman'

                    return JsonResponse(data=response, safe=False)
            else:
                response['status'] = False
                return JsonResponse(data=response, safe=False)


# 查看业务员列表
def all_salesman(request):
    response = {}
    if request.method == "GET":
        # 获取所有业务员对象
        users = models.User.objects.filter(authority="salesman")
        # 循环对象
        for user in users:
            # 获取姓名和电话
            response['user_name'] = user.user_name
            response['telephone'] = user.telephone
        return JsonResponse(data=response, safe=False)


# 查看单个业务员项目个数
def get_project_count(request):
    response = {}
    if request.method == "GET":
        # 计数器置0
        count = 0
        # 获取业务员姓名
        name = request.GET.get("user_name")
        # 获取此业务员名下的项目
        projects = models.UserProject.objects.filter(user_name=name)
        # 循环项目记数项目个数
        for project in projects:
            count += 1
        response['count'] = count
        return JsonResponse(data=response, safe=False)


# 查看项目列表
def all_project(request):
    responses = []
    if request.method == "GET":
        # 获取所有有效的项目
        projects = models.Project.objects.filter(effective=0)
        for project in projects:
            single_project_detail = {}
            # 把项目有关信息放入列表
            single_project_detail['project_id'] = project.project_id
            single_project_detail['project_name'] = project.project_name
            single_project_detail['time'] = project.time
            # 获取项目负责人信息
            names = models.UserProject.objects.filter(project_id=single_project_detail['project_id'])
            # 循环获得所有负责人姓名
            names = [name.user_name for name in names]
            single_project_detail['peoples'] = names
            responses.append(single_project_detail)
        return JsonResponse(data=responses, safe=False)


# 添加业务员
def add_salesman(request):
    response = {}
    if request.method == "POST":
        # 获取用户名和密码
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        # 随机生成一个字符串
        s = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        # 生成一个md5对象
        m = hashlib.md5()
        # 用字符串对密码进行重新编码
        new_password = s+password+s
        # 将str编码至bytes
        b = new_password.encode(encoding='utf-8')
        m.update(b)
        new_password_md5 = m.hexdigest()
        # 在数据库中保存用户名和它对应的随机字符串
        models.UserStr.objects.create(user_name=user_name, str=s)
        # 保存经过随机字符串和MD5加密后的密码
        models.User.objects.create(user_name=user_name, password=new_password_md5)
        response['status'] = True
        return JsonResponse(data=response, safe=False)

# 删除业务员
def del_salesman(request):
    responses = []
    response = {}
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user = models.User.objects.filter(user_name=user_name)
        user.delete()
        response['msg'] = "success"
        responses.append(response)
        return JsonResponse(data=responses, safe=False)


# 业务员的负责项目查询
def search_with_salesman(request):
    responses = []
    response = {}
    duty = []
    if request.method == "GET":
        name = request.GET.get("user_name")
        user_id = models.User.objects.GET(user_name=name)
        projects_id = models.UserProject.objects.filter(user_id=user_id)
        for project_id in projects_id:
            project = models.Project.objects.filter(project_id=project_id, effective=0)
            response['project_id'] = project_id
            response['project_name'] = project.project_name
            response['time'] = project.time
            users = models.UserProject.objects.filter(pro_id=project_id)
            for user in users:
                user_name = models.User.objects.filter(user_id=user.user_id)
                duty.append(user_name)
            response['user'] = duty
            responses.append(response)
        return JsonResponse(data=responses, safe=False)


# 项目搜索

# 删除业务员
def del_salesman(request):
    response = {}
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user = models.User.objects.filter(user_name=user_name)
        user.delete()
        response['status'] = True
        return JsonResponse(data=response, safe=False)


# 业务员的负责项目查询
def search_with_salesman(request):
    responses = []
    if request.method == "GET":
        # 获取业务员姓名
        name = request.GET.get("user_name")
        projects_id = models.UserProject.objects.filter(user_name=name)
        for project_id in projects_id:
            single_project = {}
            project = models.Project.objects.filter(project_id=project_id, effective=0).first()
            single_project['project_id'] = project_id
            single_project['project_name'] = project.project_name
            single_project['time'] = project.time
            users = models.UserProject.objects.filter(pro_id=project_id)
            peoples = []
            # 循环放入负责人姓名
            for user in users:
                peoples.append(user.user_name)
            single_project['peoples'] = peoples
            responses.append(single_project)
        return JsonResponse(data=responses, safe=False)


# 添加项目
def add_project(request):
    response = {}
    if request.method == "POST":
        project_name = request.POST.get("project_name")
        source = request.POST.get("source")
        introduction = request.POST.get("introduction")
        contacts = request.POST.get("contacts")
        telephone = request.POST.get("telephone")
        project = models.Project.objects.create(project_name=project_name, source=source, introduction=introduction,
                                                contacts=contacts, telephone=telephone)
        name = requests.session['user_name']
        models.UserProject.objects.create(project_id=project.project_id, user_name=name)
        response['status'] = True
        return JsonResponse(data=response, safe=False)


# 删除项目
def del_project(request):
    response = {}
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        models.Project.objects.filter(project_id=project_id).update(effective=1)
        response['status'] = True
        return JsonResponse(data=response, safe=False)


# 查看单个项目详细信息
def single_project_detail(request):
    if request.method == "GET":
        response = {}
        project_id = request.GET.get("project_id")
        project = models.Project.objects.get(project_id=project_id)

        response["project_name"] = project.project_name
        response["source"] = project.source
        response["introduction"] = project.introduction
        response["contacts"] = project.contacts
        response["telephone"] = project.telephone

        return JsonResponse(data=response, safe=False)


# 查看单个项目汇报记录
def single_project_report(request):
    responses = []
    if request.method == "GET":
        project_id = request.GET.get("project_id")
        # project = models.Project.objects.filter(project_id=project_id)
        reports = models.Report.objects.filter(project_id=project_id)
        for report in reports:
            response = {}
            # report_id，project_name，reporter，time
            response["report_id"] = report.report_id
            response["report_name"] = report.report_name
            response["reporter"] = report.reporter
            response["time"] = report.time
            responses.append(response)

        # 返回汇报列表
        return JsonResponse(data=responses, safe=False)


# 查看单个项目的老板留言
def single_project_record(request):
    responses = []
    if request.method == "GET":
        report_id = request.GET.get("report_id")
        messages = models.Message.objects.filter(report_id=report_id)
        for message in messages:
            response = {}
            response["content"] = message.content
            response["time"] = message.time
            responses.append(response)
        return JsonResponse(data=responses, safe=False)


# 留言
def record(request):
    response = {}
    if request.method == "POST":
        report_id = request.POST.get("project_id")
        content = request.POST.get("content")
        models.Message.objects.create(report_id=report_id, content=content)
        response['status'] = True
        return JsonResponse(data=response, safe=False)


# 查看单个汇报
def get_report(request):
    # responses = []
    response = {}
    if request.method == "GET":
        # 前端获取报告id
        report_id = request.GET.get("report_id")

        # 数据库查询
        report = models.Report.objects.filter(report_id=report_id)[0]

        response["project_id"] = report.project_id
        # response["report_id"] = report.id
        # response["project_name"] = project.project_name
        response["progress"] = report.progress
        response["workable"] = report.workable
        response["supply"] = report.supply
        response["capital"] = report.capital
        response["invoice"] = report.invoice
        response["other"] = report.other
        # responses.append(response)
        return JsonResponse(data=response, safe=False)


# 添加汇报
def add_report(request):
    response = {}
    if request.method == 'POST':
        # 前端获取
        report_id = request.POST.get("report_id")
        project_id = request.POST.get("project_id")
        progress = request.POST.get("progress")
        workable = request.POST.get("workable")
        supply = request.POST.get("supply")
        capital = request.POST.get("capital")
        invoice = request.POST.get("invoice")
        other = request.POST.get("other")

        # 插入数据库
        models.Report.objects.create(report_id=report_id, project_id=project_id, progress=progress,
                                     workable=workable, supply=supply, capital=capital, invoice=invoice, other=other)
        response['status'] = True
        return JsonResponse(data=response, safe=False)


# 查看老板给业务员的消息
def get_ones_record(request):
    responses = []
    if request.method == "GET":
        user_name = request.GET.get("name")

        # 先从UserProject查到名字对应的项目
        projects = models.UserProject.objects.filter(user_name=user_name)
        project_ids = [project.project_id for project in projects]

        # 通过项目查到留言
        all_message = []
        for project_id in project_ids:
            # 获取一个项目的所有消息
            one_pro_messages = models.Message.objects.filter(project_id=project_id)
            # 把一个项目的每个消息放进结果中
            for one_pro_message in one_pro_messages:
                dic = {}
                dic['message'] = one_pro_message.content
                dic['time'] = one_pro_message.time
                dic['project_id'] = one_pro_message.project_id
                all_message.append(dic)

        # 返回一个列表，列表里每个元素是消息字典
        return JsonResponse(data=all_message, safe=False)


# 老板根据key搜索项目
def search_project(request):
    if request.method == 'GET':
        key = request.GET.get('key')

        # 根据名字搜索
        projects_with_name = models.Project.objects.filter(project_name__contains=key)
        # models.Project.objects.filter()

        # 根据人搜索
        projects_id_with_people = models.UserProject.objects.filter(user_name__contains=key)
        projects_with_people = []
        for project_id in projects_id_with_people:
            projects_with_people.append(models.Project.objects.get(project_id=project_id.pro_id))

        # 把projects_with_people 和 projects_with_name合并成result
        # 按时间排序
        result = []
        index1 = 0
        index2 = 0
        while index1 < len(projects_with_people) or index2 < len(projects_with_name):
            if index2 >= len(projects_with_name) or (index1 < len(projects_with_people) and projects_with_people[index1].time > projects_with_name[index2].time):
                result.append(projects_with_people[index1])
                index1 += 1
            else:
                result.append(projects_with_name[index2])
                index2 += 1

        return JsonResponse(data=result, safe=False)