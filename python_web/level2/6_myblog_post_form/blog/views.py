from django.shortcuts import render, HttpResponse
from django.template import Template, Context
from blog.models import Article, Comment
from blog.form import CommentForm
from django.shortcuts import redirect

# Create your views here.
def home(request):
    # 调试查看request是什么参数，包括值，所有属性与方法，类型
    print(request)
    print("==="*30)
    print(dir(request))
    print("==="*30)
    print(type(request))
    print("==="*30)
    print(request.GET)
    print("==="*30)
    queryset = request.GET.get('tag') #通过GET方法获取参数tag的具体值，在url中输入?tag=test123,则此处获取的queryset即为test123
    print(queryset)
    

    if queryset:   #如果不为空，即传递tag值，则加载分类页面
        article_set = Article.objects.filter(tag=queryset) #过滤出'tag值'为'url中传递的参数'的所有数据表
    else:          #如果为空，即加载所有数据页面
        article_set = Article.objects.all()

    context = {
        'template_article':article_set,
    }
    web = render(request,'first_web_2.html',context)
    return web

def details(request):
    context = {}
    comments_set = Comment.objects.all()
    context['comments_set'] = comments_set

    if request.method == 'GET':
        form = CommentForm  #实例化一个CommentForm
    if request.method == 'POST': #提交表单form时都是使用的POST方法
        form = CommentForm(request.POST)   #1:绑定表单:将请求的POST数据装载在CommentForm实例中，只有在绑定了表单才可以验证数据
        # 2.验证表单：验证表单是否通过，如果通过则进行下面操作，表单数据会被存储在字典变量中
        if form.is_valid():
            name = form.cleaned_data['name'] #取出表单中完成验证的数据（字典变量），将字典中key值为name的变量存储在name中
            comment = form.cleaned_data['comment'] #取出表单中完成验证的数据（字典变量），将字典中key值为comment的变量存储在comment中
            c = Comment(name=name,comment=comment) #实例化Comment类，初始化其两个变量
            c.save() #存储到数据库中
            return redirect(to='details') #跳转到url.py中name=details的URL中

    context['form'] = form #将表单填入到上下文

    return render(request,'detail.html',context)

