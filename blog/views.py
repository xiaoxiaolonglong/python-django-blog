# 添加一个函数
import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from myblog.settings import ALLOW_CROSS
from .models import Article, Category, Tag, Link, Banner


def index(request):
    # 对Article进行声明并实例化，然后生成对象allarticle
    allarticle = Article.objects.all()
    # 把查询到的对象，封装到上下文
    context = {
        'allarticle': allarticle,
    }
    # 把上传文传到模板页面index.html里
    return render(request, 'index.html', context)


def get_all(request):
    # 对Article进行声明并实例化，然后生成对象allarticle
    allarticle = Article.objects.all()
    res = serializers.serialize("json", allarticle, fields=('title', 'user', 'tags'))  # 把所有Person对象序列化
    response = HttpResponse(json.dumps(json.loads(res), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS == True:
        response["Access-Control-Allow-Origin"] = "*"
    return response


# 获取所有文章分类
def get_all_category(request):
    if request.method == 'GET':
        category = Category.objects.all()
        data = serializers.serialize("json", category, fields=('index', 'name'))  # 对象序列化
        res = {'code': '1', 'msg': '文章分类查询成功', 'data': json.loads(data)}
    else:
        res = {'code': '0', 'msg': '文章分类查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response


# 获取推荐位
def get_tui_by_count(request):
    # 1.热门推荐
    # 2.推荐阅读
    if request.method == 'GET':
        tui_id = request.GET.get("tui_id")
        count = request.GET.get("count")
        tui = Article.objects.filter(tui_id=tui_id).order_by("-created_time")[:int(count)]
        data = serializers.serialize("json", tui, fields=('title','img', 'excerpt','created_time'))  # 对象序列化
        res = {'code': '1', 'msg': '首页推荐阅读查询成功', 'data': json.loads(data)}
    else:
        res = {'code': '0', 'msg': '首页推荐阅读查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response


# 获取首页最新文章
def get_new_article(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by("-created_time")[:10]
        category = Category.objects.all()
        articleList = serializers.serialize("json", articles, fields=('title','img','category', 'excerpt','created_time'))  # 对象序列化
        categoryList = serializers.serialize("json", category, fields=('index', 'name'))
        data = {'article':json.loads(articleList),'category':json.loads(categoryList)}
        res = {'code': '1', 'msg': '最新文章查询成功', 'data': data}
    else:
        res = {'code': '0', 'msg': '最新文章查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response

# 获取首页热门文章
def get_hot_article(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('views')[:10]#通过浏览数进行排序
        articleList = serializers.serialize("json", articles, fields=('title','img','category', 'excerpt','created_time'))  # 对象序列化
        res = {'code': '1', 'msg': '热门文章查询成功', 'data': json.loads(articleList)}
    else:
        res = {'code': '0', 'msg': '热门文章查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response

# 获取所有标签
def get_all_tag(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        list = serializers.serialize("json", tags, fields=('name'))  # 对象序列化
        res = {'code': '1', 'msg': '所有标签查询成功', 'data': json.loads(list)}
    else:
        res = {'code': '0', 'msg': '所有标签查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response

# 获取友情链接
def get_all_link(request):
    if request.method == 'GET':
        links = Link.objects.all()
        list = serializers.serialize("json", links, fields=('name','linkurl'))  # 对象序列化
        res = {'code': '1', 'msg': '所有标签查询成功', 'data': json.loads(list)}
    else:
        res = {'code': '0', 'msg': '所有标签查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response

# 获取banner
def get_banner(request):
    if request.method == 'GET':
        banners = Banner.objects.all()
        list = serializers.serialize("json", banners)  # 对象序列化
        res = {'code': '1', 'msg': '所有标签查询成功', 'data': json.loads(list)}
    else:
        res = {'code': '0', 'msg': '所有标签查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response