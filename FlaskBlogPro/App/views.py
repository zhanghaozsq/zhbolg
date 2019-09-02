# url+视图函数
from flask import Blueprint, render_template, request, redirect,jsonify
from .models import *

blog = Blueprint('blog', __name__)
admin = Blueprint('admin', __name__)


@blog.route('/')
def home():
    return 'HOME'

##################################################################################
##后台
##################################################################################
# 管理首页
@admin.route('/admin/')
def amdin_index():
    return render_template('admin/index.html')


# 文章管理
@admin.route('/article/')
def amdin_article():
    return redirect('/article/1/')

@admin.route('/article/<int:page>/')
def amdin_article_page(page=None):
    per_page = 2
    if not page:
        page = 1
    articles = Article.query.all()
    articles = articles[(page-1)*per_page:page*per_page]
    my_paginate = Article.query.order_by('id').paginate(page=page,per_page=per_page)

    return render_template('admin/article.html',articles=articles,my_paginate=my_paginate)

# 删除文章
@admin.route('/article/delete/',methods=['POST'])
def article_delete():
    id = request.form.get('id')
    article = Article.query.get(id)
    if article:
        try:
            db.session.delete(article)
            db.session.commit()
            code = 1
            msg = 'delete success'
        except:
            db.session.rollback()
            db.session.flush()
            code = 0
            msg = 'delete fail'

    else:
        code = 0
        msg = 'not id'
    data = {
        'code': code,
        'msg': msg,
    }
    print(data)
    return jsonify(data)

# 修改文章
@admin.route('/update/article/',methods=['GET','POST'])
def update_article():
    if request.method == 'GET':
        id = request.args.get('id')
        article = Article.query.get(id)
        categorys = Category.query.all()
        if article:
            return render_template('admin/update-article.html',article=article,categorys=categorys)
        return 'fail'
    else:
        id = request.form.get('id')
        print(id)
        article = Article.query.get(id)
        if article:
            try:
                article.title = request.form.get('title')
                article.content = request.form.get('content')
                article.categoryid = request.form.get('category')
                article.describe = request.form.get('describe')
                article.keywords = request.form.get('keywords')
                article.titlepic = request.form.get('titlepic')
                article.visibility = request.form.get('visibility')
                db.session.commit()
                return redirect('/article/')
            except:
                db.session.rollback()
                db.session.flush()
                return 'update fail'

        else:
            return 'not article'

# 增加文章链接
@admin.route('/addarticle/')
def amdin_addarticle():
    categorys = Category.query.all()
    data = {
        'categorys':categorys
    }
    return render_template('admin/add-article.html',data=data)

# 增加文章
@admin.route('/Article/add',methods=['POST','GET'])
def amdin_articleadd():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            print(title)
            user = Article.query.filter_by(title=title).first()
            if user:
                print(user.all())
                return '标题重复'
            content = request.form.get('content')
            keywords = request.form.get('keywords')
            describe = request.form.get('describe')
            category = request.form.get('category')
            tags = request.form.get('tags')
            # tags = request.form.get('tags')
            visibility = request.form.get('visibility')

            
            article = Article()
            article.title = title
            article.content = content
            article.keywords = keywords
            article.describe = describe
            article.categoryid = category
            article.tags = tags
            article.visibility = visibility
            db.session.add(article)
            db.session.commit()
            return redirect('/article/')
        except:
            # 回滚
            db.session.rollback()
            db.session.flush()
            return 'No'
    return '请求方式错误'


# 栏目管理
@admin.route('/category/')
def amdin_category():
    categorys = Category.query.all()
    data = {
        'categorys':categorys,
    }
    return render_template('admin/category.html',data=data)

# 修改栏目
@admin.route('/update/category/',methods=['GET','POST'])
def update_category():
    if request.method == 'GET':
        id = request.args.get('id')
        category = Category.query.get(id)
        if category:
            categorys = Category.query.filter(Category.id != id)
            data = {
                'categorys': categorys,
                'category':category,
            }
            return render_template('admin/update-category.html',data=data)
        return 'fail'
    else:
        id = request.form.get('id')
        print(id)
        category = Category.query.get(id)
        if category:
            try:
                category.name = request.form.get('name')
                category.keywords = request.form.get('keywords')
                category.fid = request.form.get('fid')
                category.describe = request.form.get('describe')
                category.alias = request.form.get('alias')
                db.session.commit()
                return redirect('/category/')
            except:
                db.session.rollback()
                db.session.flush()
                return 'update fail'

        else:
            return 'not category'


# 增加栏目
@admin.route('/category/add/',methods=['GET','POST'])
def amdin_category_add():
    # 得到新栏目的数据
    # 名字
    name = request.form.get('name')
    category = Category.query.filter_by(name=name).first()
    if category:
        return '栏目名重复'
    # 别名
    alias = request.form.get('alias')
    # 父节点
    fid = request.form.get('fid')
    # 关键字
    keywords = request.form.get('keywords')
    # 描述
    describe = request.form.get('describe')
    try:
        category = Category()
        category.name = name
        category.alias = alias
        category.fid = fid
        category.keywords = keywords
        category.describe = describe
        db.session.add(category)
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        db.session.flush()
        return 'fail'

    return redirect('/category/')

# 删除栏目
@admin.route('/category/delete/',methods=['POST'])
def amdin_category_delete():
    id = request.form.get('id')
    category = Category.query.get(id)
    if category:
        try:
            db.session.delete(category)
            db.session.commit()
            code = 1
            msg = 'delete success'
        except:
            db.session.rollback()
            db.session.flush()
            code = 0
            msg = 'delete fail'

    else:
        code = 0
        msg = 'not id'
    data = {
        'code':code,
        'msg':msg,
    }
    print(data)
    return jsonify(data)
    # return redirect('/category/')
# 公告管理
@admin.route('/notice/')
def amdin_notice():
    return render_template('admin/notice.html')

# 增加公告
@admin.route('/addnotice/')
def amdin_addnotice():
    return render_template('admin/add-notice.html')

# 评论管理
@admin.route('/comment/')
def amdin_comment():
    return render_template('admin/comment.html')

# 用户管理
@admin.route('/manageuser/')
def amdin_manageuser():
    return render_template('admin/manage-user.html')

# 管理登录日志
@admin.route('/loginlog/')
def amdin_loginlog():
    return render_template('admin/loginlog.html')

# 基本设置
@admin.route('/setting/')
def amdin_setting():
    return render_template('admin/setting.html')

# 阅读设置
@admin.route('/readset/')
def amdin_readset():
    return render_template('admin/readset.html')

# 友情链接
@admin.route('/flink/')
def amdin_flink():
    return render_template('admin/flink.html')

# 增加友情链接
@admin.route('/addflink/')
def amdin_addflink():
    return render_template('admin/add-flink.html')


##################################################################################
##前台
##################################################################################
# 网站首页
@blog.route('/index/')
def index():
    try:
        # 显示所有分类
        categorys = Category.query.filter()
        # 显示所有文章
        articles = Article.query.all()
        # 汇总
        # c_count = []
        # for category in categorys:
        #     t = category.articles.count()
        #     c_count.append(t)
        data = {
            'categorys': categorys,
            'articles': articles,
            # 'count':c_count,
        }
    except:
        return 'fail'
    return render_template('blog/index.html',data=data)

# 分类
@blog.route('/blogcategory/')
def blog_category():
    # per_page = 1
    id = request.args.get('id')
    # page = request.args.get('page')
    # if not page:
    #     page = 1
    if not id:
        # articles = Article.query.order_by('id').paginate(page=page,per_page=per_page)
        articles = Article.query.all()

    else:
        # articles = Article.query.filter_by(categoryid=id).order_by('id').paginate(page=page,per_page=per_page)
        articles = Article.query.filter_by(categoryid=id).all()
    categorys = Category.query.all()

    data = {
        'articles':articles,
        'categorys':categorys
    }
    # return jsonify(data)
    return render_template('blog/list.html',data=data)

# 详情
@blog.route('/blogdetail/')
def blog_detail():
    id = request.args.get('id')
    if not id:
        id = 1
    article = Article.query.get(id)
    categorys = Category.query.all()
    data = {
        'article': article,
        'category':article.category.name,
        'categorys':categorys,
    }
    return render_template('blog/info.html',data=data)

# 我的相册
@blog.route('/share/')
def share():
    return render_template('blog/share.html')

# 我的日记
@blog.route('/list/')
def list():
    return redirect('/blogcategory/')

# 关于我
@blog.route('/about/')
def about():
    return render_template('blog/about.html')

# 留言
@blog.route('/gbook/')
def gbook():
    return render_template('blog/gbook.html')

# 内容页
@blog.route('/info/')
def info():
    return redirect('/blogdetail/')

# 详情页
@blog.route('/infopic/')
def infopic():
    return render_template('blog/infopic.html')