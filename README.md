# CURD
- Create : 생성 ex.로그인
- Read(or retrieve) : 읽기(인출) ex.로그인
- Update : 갱신 ex.새로운 사진으로 프로필 바꾸기
- Delete(or destroy) : 삭제(파괴) ex.계정탈퇴

## 00. setting
- 가상환경 생성
```shell
python -m venv venv
```
- 가상환경 활성화
```shell
source venv/Scripts/activate
```
- `.gitignore` 설정 : python, windows, macOS, Django

## 01. Django
- 현재 폴더에 django 설치
```shell
pip install django
```
- 현재 폴더(.)에 crud 프로젝트 생성
```shell
django-admin startproject crud .
```
- 앱 생성
```shell
django-admin startapp posts
```
- `/crud/settings.py`에 `INSTALLED_APPS = [ , 'posts', ]` 추가 : 앱 등록
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
]
```

1. `crud/urls.py`에 `urlpatterns`의 리스트에 `path('index/', views.index)`추가 => views 선언해야함

2. `crud/urls.py`에 `from posts import views` 선언
```python
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
]
```

3. `posts/views.py`에 index함수 정의 => `index.html`파일 만들어야함
```python
def index(request):
    return render(request, 'index.html')
```

4. `post`폴더 안에 `templates`폴더 만들기

5. `templates`폴더 안에 `index.html`파일 생성 후 보여줄 내용 작성
```html
<body>
    <h1>index</h1>
</body>
```

## 02.CRUD
- ORM(Object-Relational Mapping)
    - O : python 세상
    - RM : SQL 세상
- **modeling** : 스키마 정의
    - `posts/models.py` : 클래스 정의
    - [CharField](https://docs.djangoproject.com/en/5.1/ref/forms/fields/#django.forms.CharField)
    ```python
    class Post(models.Model): # models안의 Model클래스 사용
        title = models.CharField(max_length=100) # 글자 저장 필드
        content = models.TextField()
    ```
    - 클래스는 단수(하나하나의 정의를 나타냄), 첫글자 대문자

- **migration** : python세상에서 SQL세상(`db.sqlite3`)으로 이주
```shell
# 번역본 생성
python manage.py makemigrations
# => `posts/migrations/0001_initial.py` 생성 : SQL에 반영할 수 있는 python 문서
```
```shell
# DB에 반영
python manage.py migrate
```
    - Extensions -> `SQLite Viewer` 프로그램 설치\
    => db.sqlite3파일 모양이 바뀜\
    => 들어가보면 `posts_post`가 우리가 만든 파일

### **create super user**
- `admin/` 계정 생성
```shell
python manage.py createsuperuser
# Username : admin
# Email address : 
# password : 1234
# password(again) : 1234
# y
```
    - `python manage.py runserver` 실행 후 위에서 만든 아이디와 비밀번호로 로그인하면 관리자 페이지가 뜸(정보를 볼 수 있음)\
    => password는 암호화되어 저장되어있음

### **admin페이지(관리자 페이지)에 모델 등록** (`admin.py`)
```python
from django.contrib import admin
from .models import Post
# admin과 같은 위치에 있기 때문에 .models
# Register your models here.
admin.site.register(Post)
```

### Read
- `Post`클래스 `views.py`에 불러와서 사용
```python
from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    #데이터 접근
    posts = Post.objects.all() # Post클래스의 모든 데이터를 다 가져오기
    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context)
```
- posts를 출력해보면 QuerySet으로 Object가 묶여있음
```html
<body>
    <h1>index</h1>
    {% for post in posts %}
        <p>{{post.title}}</p>
        <p>{{post.content}}</p>
        <hr>
    {% endfor %}
</body>
```
=> Object 따로 출력
- 주의 :  `models.py`에서 오타나거나 잘못입력했다면 수정하고 다시 번역본 만들고 read해야함


### 하나의 게시물에 상세보기 페이지 만들기
- `urls.py`파일에 경로 추가
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    # `index/`를 `posts/`로 바꿈 => `views.py`에 delete함수랑 `detail.html`에 home링크도 수정하기
    path('index/', views.index), # 게시물 전체 목록을 보여주는 페이지
    path('posts/<int:id>/', views.detail), # id : 게시물의 고유한 번호 => django가 자동으로 설정
]
```
=> `posts/1/`, `posts/2/`, `posts/10/` 모두 `path('posts/<int:id>/', views.detail)`가 처리
- `views.py`에 `detail`함수 추가
```python
def detail(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post,
    }
    return render(request, 'detail.html', context)
```
- `detail.html`파일 만들기
```html
<body>
    <h1>detail</h1>
    <h3>{{post.title}}</h3>
    <p>{{post.content}}</p>
</body>
```
- index링크에서 하나의 object링크로 이동(`index.html`)
```html
<body>
    <h1>index</h1>
    {% for post in posts %}
        <p>{{post.title}}</p>
        <p>{{post.content}}</p>
        <!--각 post 링크로 이동-->
        <a href="/posts/{{post.id}}/">detail</a>
        <hr>
    {% endfor %}
</body>
```
- object링크에서 index링크로 돌아가기(`detail.html`)
```html
<body>
    <h1>detail</h1>
    <h3>{{post.title}}</h3>
    <p>{{post.content}}</p>
    <!--index페이지로 돌아가기-->
    <a href="/index/">home</a>
</body>
```

### Create
- 게시물 생성하기
1. 사용자에게 빈 종이 제공
    - `urls.py`
    ```python
    urlpatterns = [
        path('admin/', admin.site.urls),
        # Read(ALL) - 몇 번 게시물을 읽어줘
        path('posts/', views.index),
        # Read(1)
        path('posts/<int:id>/', views.detail),
        # Create
        path('posts/new/', views.new),
        path('posts/create/', views.create),
    ]
    ```
    - `views.py`
    ```python
    def new(request):
        return render(request, 'new.html')
    
    def create():
        pass
    ```
2. 빈 종이에 내용 입력
    - `new.html`
    ```html
    <body>
        <form action="">
            <input type="text" name="title">
            <input type="text" name="content">
            <input type="submit">
        </form>
    </body>
    ```
3. 입력된 내용 `/posts/create/`로 전송
    - `<form action="/posts/create/">` 추가
4. 전송된 데이터 중 필요한 정보 뽑아내기
    - `views.py`
    ```python
    def create(request):
        title = request.GET.get('title')
        content = request.GET.get('content')
        # 파이썬 객체 object
        post = Post() # Post클래스 인스턴스화해서 post에 담기
        post.title = title 
        post.content = content
    ```
5. DB에 저장
    - `post.save()` 추가
    ```python
    def create(request):
        title = request.GET.get('title')
        content = request.GET.get('content')
        # 파이썬 객체 object
        post = Post() # Post클래스 인스턴스화해서 post에 담기
        post.title = title 
        post.content = content
        # 데이터 저장 - id를 만들어줌
        post.save()
    ```
6. 사용자에게 저장된 내용 보여주기
    - `redirect` : 사용자가 요청한 URL이 아닌 다른 URL로 이동
    ```python
    from django.shortcuts import render, redirect

    def create(request):
        title = request.GET.get('title')
        content = request.GET.get('content')
        # 파이썬 객체 object
        post = Post() # Post클래스 인스턴스화해서 post에 담기
        post.title = title 
        post.content = content
        # 데이터 저장 - id를 만들어줌
        post.save()

        # return redirect('/index/')
        return redirect(f'/posts/{post.id}/') # 변수화된 데이터 사용
        # 제출하면 방금 만든 게시물페이지로 이동
    ```


### Delete
1. 사용자가 삭제 버튼 클릭
- `detail.html`에 삭제 버튼 추가
    ```html
    <body>
        <h1>detail</h1>
        <h3>{{post.title}}</h3>
        <p>{{post.content}}</p>
        <!--index페이지로 돌아가기-->
        <a href="/posts/">home</a>
        <a href="/posts/{{post.id}}/delete/">delete</a>
    </body>
    ```
- `urls.py`에 경로 설정
    ```python
    urlpatterns = [
        path('admin/', admin.site.urls),
        # Read(ALL) - 몇 번 게시물을 읽어줘
        path('posts/', views.index), # 게시물 전체 목록을 보여주는 페이지
        # Read(1)
        path('posts/<int:id>/', views.detail), # id : 게시물의 고유한 번호 => django가 자동으로 설정
        # Create
        path('posts/new/', views.new),
        path('posts/create/', views.create),
        # Delete - 몇 번 게시물을 지워줘
        path('posts/<int:id>/delete/', views.delete),
    ]
    ```
2. 몇 번 게시물을 삭제할지 찾기
- `views.py`
    ```python
    def delete(request, id):
        post = Post.objects.get(id=id)
    ```
3. 해당 게시물 삭제
- `views.py`
    ```python
    def delete(request, id):
        post = Post.objects.get(id=id)
        post.delete()
        return  redirect('/index/')
    ```


### Update
1. 사용자가 수정 버튼 클릭
- `detail.html`에 수정 버튼 추가
    ```html
    <body>
        <h1>detail</h1>
        <h3>{{post.title}}</h3>
        <p>{{post.content}}</p>
        <!--index페이지로 돌아가기-->
        <a href="/posts/">home</a>
        <a href="/posts/{{post.id}}/delete/">delete</a>
        <a href="/posts/{{post.id}}/edit/">update</a>
    </body>
    ```
2. 몇 번 게시물을 수정할지 찾기
- `urls.py`
    ```python
    urlpatterns = [
        path('admin/', admin.site.urls),
        # Read(ALL) - 몇 번 게시물을 읽어줘
        path('posts/', views.index), # 게시물 전체 목록을 보여주는 페이지
        # Read(1)
        path('posts/<int:id>/', views.detail), # id : 게시물의 고유한 번호 => django가 자동으로 설정
        # Create
        path('posts/new/', views.new),
        path('posts/create/', views.create),
        # Delete - 몇 번 게시물을 지워줘
        path('posts/<int:id>/delete/', views.delete),
        # Update - create + read, 몇 번 게시물을 수정해줘
        path('posts/<int:id>/edit/', views.edit),
        path('posts/<int:id>/update/', views.update),
    ]
    ```
- `views.py`
    ```python
    def edit(request, id): # detail함수와 똑같지만 edit은 수정할 수 있게 html을 만들어줌
        post = Post.objects.get(id=id)
        context = {
            'post': post,
        }
        return render(request, 'edit.html', context)

    def update():
        pass
    ```
3. 해당 게시물에 전에 제출했던 내용이 들어있어야함
- `edit.html`
    ```html
    <body>
        <h1>edit</h1>
        <form action="">
            <input type="text" value="{{post.title}}" name="title">
            <input type="text" value="{{post.content}}" name="content">
            <input type="submit">
        </form>
    </body>
    ```
4. `/posts/{{post.id}}/update/`로 전송
- `edit.html`파일에 `<form action="/posts/{{post.id}}/update/">`추가
    ```html
    <body>
        <h1>edit</h1>
        <form action="/posts/{{post.id}}/update/">
            <input type="text" value="{{post.title}}" name="title">
            <input type="text" value="{{post.content}}" name="content">
            <input type="submit">
        </form>
    </body>
    ```
3. 해당 게시물 수정
- `views.py`
    ```python
    def update(request, id):
        # 기존정보 가져오기
        post = Post.objects.get(id=id)

        # 새로운 정보 가져오기
        title = request.GET.get('title')
        content = request.GET.get('content')

        # 기존정보를 새로운정보로 바꾸기
        post.title = title
        post.content = content
        post.save()

        return redirect(f'/posts/{post.id}/')
    ```