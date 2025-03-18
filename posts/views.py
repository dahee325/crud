from django.shortcuts import render, redirect
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context)

def detail(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post,
    }
    return render(request, 'detail.html', context)

def new(request):
    return render(request, 'new.html')

def create(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    # 파이썬 객체 object
    post = Post() # Post클래스 인스턴스화해서 post에 담기
    post.title = title 
    post.content = content
    # 데이터 저장
    post.save()

    # return redirect('/index/')
    return redirect(f'/posts/{post.id}/') # 변수화된 데이터 사용
    # 제출하면 방금 만든 게시물페이지로 이동