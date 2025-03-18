# CURD
- create : 생성 ex.로그인
- read(or retrieve) : 읽기(인출) ex.로그인
- update : 갱신 ex.새로운 사진으로 프로필 바꾸기
- delete(or destroy) : 삭제(파괴) ex.계정탈퇴

## 00. setting
- `python -m venv venv` : 가상환경 생성
- `source venv/Scripts/activate` : 가상환경 활성화
- `.gitignore` 설정 : python, windows, macOS, Django

## 01. Django
- `pip install django` : 현재 폴더에 django 설치
- `django-admin startproject crud .` : 현재 폴더(.)에 crud 프로젝트 생성
- `django-admin startapp posts` : 앱 생성
- `/crud/settings.py`에 `INSTALLED_APPS = [ , 'posts', ]` 추가 : 앱 등록

1. `crud/urls.py`에 `urlpatterns`의 리스트에 `path('index/', views.index)`추가 => views 선언해야함

2. `crud/urls.py`에 `from posts import views` 선언
```python
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index)
]
```

3. `posts/views.py`에 index함수 정의 => `index.html`파일 만들어야함
```python
def index(request):
    return render(request, 'index.html')
```

4. `post`폴더 안에 `templates`폴더 만들기

5. `templates`폴더 안에 `index.html`파일 생성 후 보여줄 내용 작성

## 02.CRUD
- ORM(object relative mapping)
    - O : python 세상
    - RM : SQL 세상
- modeling : 스키마 정의
    - `posts/models.py` : 클래스 정의
    - [CharField](https://docs.djangoproject.com/en/5.1/ref/forms/fields/#django.forms.CharField)
    ```python
    class Post(models.Model): # models안의 Model클래스 사용
    title = models.CharField(max_length=100) # 글자 저장 필드
    content = models.TextField()
    ```
    - 클래스는 단수(하나하나의 정의를 나타냄), 첫글자 대문자

- migration : python세상에서 SQL세상(`db.sqlite3`)으로 이주
```shell
# 번역본 생성
python manage.py makemigrations
# => `posts/migrations/0001_initial.py` 생성 : SQL에 반영할 수 있는 python 문서
```
```shell
# DB에 반영
`python manage.py migrate`
```