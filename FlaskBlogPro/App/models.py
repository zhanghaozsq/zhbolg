# 模型
from .exts import db

# # 文章分类表
# class ArticleType(db.Model):
#     __tablename__ = 'ArticleType'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50))
#     articles = db.relationship("Article", backref="articletype", lazy=True)
#
#
# #  文章表
# class Article(db.Model):
#     __tablename__ = 'Article'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100))
#     content = db.Column(db.Text)
#     create_time = db.Column(db.DateTime)
#     click_num = db.Column(db.Integer, default=0)
#     description = db.Column(db.String(200))
#     img = db.Column(db.String(255), default="")
#     article_type = db.Column(db.Integer, db.ForeignKey("ArticleType.id"))

# 文章分类
class Category(db.Model):
    # 表名
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 栏目名称
    name = db.Column(db.String(30), unique=True)
    # 栏目别名
    alias = db.Column(db.String(30), unique=True,nullable=True)
    # 父节点
    fid = db.Column(db.Integer,nullable=True)
    # 关键字
    keywords = db.Column(db.String(50),nullable=True)
    # 描述
    describe = db.Column(db.Text)
    # 一个分类有多个文章
    articles = db.relationship('Article', backref='category', lazy=True)

# 文章
class Article(db.Model):
    # 表名
    __tablename__ = 'Article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(50), unique=True)
    # 内容
    content = db.Column(db.Text)
    # 标题图片
    titlepic = db.Column(db.String(50),nullable=True)
    # 描述
    describe = db.Column(db.Text,nullable=True)
    # 关键字
    keywords = db.Column(db.String(50),nullable=True)
    # 标签
    tags = db.Column(db.String(30),nullable=True)
    # 状态
    visibility = db.String(db.Boolean)
    # 创建外键,关联到分类表的主键，实现一对多关系
    categoryid = db.Column(db.Integer, db.ForeignKey(Category.id))



