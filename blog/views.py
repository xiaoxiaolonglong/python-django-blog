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
        category = Category.objects.values()
        res = {'code': '1', 'msg': '文章分类查询成功', 'data': list(category)}
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
        tui = Article.objects.values('id','title','img', 'excerpt').filter(tui_id=tui_id).order_by("-created_time")[:int(count)]
        res = {'code': '1', 'msg': '首页推荐阅读查询成功', 'data': list(tui)}
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
        articles = Article.objects.values('id', 'title', 'img','category','category__name', 'excerpt', 'created_time').order_by(
            "-created_time")[:10]
        data = list(articles)
        for article in data:
            article['created_time'] = article['created_time'].strftime('%Y-%m-%d %H:%M:%S')
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
        articles = Article.objects.values('id','title','img', 'excerpt').order_by('views')[:10]#通过浏览数进行排序
        res = {'code': '1', 'msg': '热门文章查询成功', 'data': list(articles)}
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
        tags = Tag.objects.values()
        res = {'code': '1', 'msg': '所有标签查询成功', 'data': list(tags)}
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
        links = Link.objects.values()
        res = {'code': '1', 'msg': '所有标签查询成功', 'data':list(links)}
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
        banners = Banner.objects.values()
        res = {'code': '1', 'msg': '所有标签查询成功', 'data': list(banners)}
    else:
        res = {'code': '0', 'msg': '所有标签查询失败！', 'data': []}
    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response


# 文章列表，三个参数：1.分类：category，2.标签：tag，3.页数
def get_article(request):
    if request.method == 'GET':
        category_id = request.GET.get('category')
        if category_id is '':
            category_id = None;
        tag_id = request.GET.get('tag')
        if tag_id is '':
            tag_id = None;
        page = request.GET.get('page')
        if page is None:
            page = 0;
        else:
            page = int(page) - 1
        pagesize = 10
        pagecount = 0
        articles = []
        navbar = ""
        if category_id is not None:
            navbar = Category.objects.values().filter(id=category_id)
            articles = Article.objects.values('id', 'title', 'img','category','category__name', 'excerpt', 'created_time').filter(category=category_id).order_by('-created_time')[page*pagesize:(page+1)*pagesize]
            pagecount = len(list(Article.objects.values('id', 'title').filter(category=category_id)))
        elif tag_id is not None:
            articles = Article.objects.values('id', 'title', 'img','category','category__name', 'excerpt', 'created_time').filter(tags__id=tag_id).order_by('-created_time')[page*pagesize:(page+1)*pagesize]

        data = list(articles)
        for article in data:
            article['created_time'] = article['created_time'].strftime('%Y-%m-%d %H:%M:%S')
        res = {'code': '1', 'msg': '文章列表查询成功','navbar':list(navbar), 'data': data,'pagecount':pagecount,'pageindex':page+1,'pagesize':pagesize}
    else:
        res = {'code': '0', 'msg': '文章列表查询失败！', 'data': []}

    response = HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if ALLOW_CROSS:
        response["Access-Control-Allow-Origin"] = "*"
    return response