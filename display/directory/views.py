import json, os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
from .show_dir import get_origin_dirs

def get_path(path):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)

def sort(directory):
    if directory["child_dirs"]:
        directory["child_dirs"] = sorted(directory["child_dirs"], key=lambda x: x['dirname'])
        for dir in directory["child_dirs"]:
            dir["files"] = sorted(dir["files"], key=lambda x: x["filename"])
    if directory["files"]:
        directory["files"] = sorted(directory["files"], key=lambda x: x['filename'])
    return directory

def check_login(f):
    @wraps(f)
    def inner(request, *arg, **kwargs):
        if request.session.get('is_login') == '1':
            return f(request, *arg, **kwargs)
        else:
            return redirect('/login')
    return inner

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        language = request.POST.get('language')
        tag = request.POST.get('tag')
        if tag:
            return render(request, 'login.html', {"language": language})
        else:
            with open(get_path('account.txt'), 'r', encoding='utf-8') as account:
                for item in account.readlines():
                    user = json.loads(item)
                    if user['username'] == username and user['password'] == password:
                        request.session['is_login'] = '1'
                        request.session['user_id'] = user['id']
                        directory = sort(get_origin_dirs('pdf'))
                        child_dirs = []
                        for child in directory["child_dirs"]:
                            child_dir = {'dirname': child['dirname'], 'dirname_s': child['dirname_s']}
                            child_dirs.append(child_dir)
                        return render(request, 'index.html', {"username": username, "directory": directory, "child_dirs": child_dirs, "language": language})
                return render(request, 'login.html', {"flag": "用户名或密码错误！", "language": language})
    else:
        return render(request, 'login.html')

@check_login
def index(request):
    if request.method == "GET":
        user_id = request.session.get('user_id')
        with open(get_path('account.txt'), 'r', encoding='utf-8') as account:
            for item in account.readlines():
                user = json.loads(item)
                if user['id'] == user_id:
                    username = user['username']
                    directory = sort(get_origin_dirs('pdf'))
                    child_dirs = []
                    for child in directory["child_dirs"]:
                        child_dir = {'dirname': child['dirname'], 'dirname_s': child['dirname_s']}
                        child_dirs.append(child_dir)
                    return render(request, 'index.html', {"username": username, "directory": directory, "child_dirs": child_dirs})
        return render(request, 'index.html', {"username": ""})
    else:
        username = request.POST.get('username')
        item = request.POST.get('item')
        language = request.POST.get('language')
        if 'pdf' in item:
            directory = sort(get_origin_dirs('pdf'))
            child_dirs = []
            for child in directory["child_dirs"]:
                child_dir = {'dirname': child['dirname'], 'dirname_s': child['dirname_s']}
                child_dirs.append(child_dir)
            return render(request, 'index.html', {"username": username, "directory": sort(get_origin_dirs(item)), "child_dirs": child_dirs, "language": language})
        else:
            return render(request, 'index.html', {"username": username, "directory": sort(get_origin_dirs(item)), "language": language})