# CURD

## 00. setting
- `python -m venv venv` : 가상환경 생성
- `source venv/Scripts/activate` : 가상환경 활성화
- `.gitignore` 설정 : python, windows, macOS, Django

## 01. Django
- `pip install django` : 현재 폴더에 django 설치
- `django-admin startproject crud .` : 현재 폴더(.)에 crud 프로젝트 생성
- `django-admin startapp posts` : 앱 생성
- `/crud/settings.py`에 앱 등록