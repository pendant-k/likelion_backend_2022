from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import random
# Create your views here.
nextId = 4
topics = [{"id": 1, "title": "routing", "body": "Routing is..."}, {
    "id": 2, "title": "view", "body": "View is..."}, {"id": 3, "title": "Model", "body": "Model is..."}]


def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li>
                <a href="/update/{id}">update</a>
            </li>
            '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return HttpResponse(f'''
    <html>
    <body>
        <h1><a href="/"> Django </a></h1>
        <ol>
            {ol}
        </ol>
        {articleTag}
        <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}
        </ul>
    </body>
    </html>
''')


def index(request):
    article = '''
        <h2>Welcome</h2>
        Hello, Django
    '''
    return HTMLTemplate(article)


@csrf_exempt
def create(request):
    global nextId
    # check method
    print('request.method', request.method)
    if request.method == 'GET':
        article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HTMLTemplate(article)
    elif request.method == 'POST':
        print(request.POST['title'])
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id": nextId, "title": title, "body": body}
        topics.append(newTopic)
        url = '/read/' + str(nextId)
        nextId += 1
        return redirect(url)


@csrf_exempt
def delete(request):
    global topics
    if request.method == "POST":
        id = request.POST['id']
        if id == "None":
            return redirect('/')
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
    return redirect('/')


def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HTMLTemplate(article, id)


## 직접 만들어본 update 기능 
def get_update(request, id):
    global topics
    if request.method == 'GET':
        topic_id = int(id) - 1
        current_topic = topics[topic_id]
        title = current_topic['title']
        print(title)
        body = current_topic['body']
        article = f'''
        <form action="/update/" method="post">
            <p><input type="text" name="title" placeholder="title" value={title}></p>
            <p><textarea name="body" placeholder="body">{body}</textarea></p>
            <p><input type="submit"></p>
            <input type="hidden" name="id" value={id}>
        </form> 
        '''
        return HTMLTemplate(article)


@csrf_exempt
def post_update(request):
    global topics
    if request.method == 'POST':
        topic_id = request.POST['id']
        title = request.POST['title']
        body = request.POST['body']
        topics[int(topic_id)-1]['title'] = title
        topics[int(topic_id)-1]['body'] = body
        url = '/read/' + str(topic_id)
        return redirect(url)

## 답안지
@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title": topic['title'],
                    "body": topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selectedTopic['title']}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form> 
        '''
        return HTMLTemplate(article)
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')

# 더 나아가기
# 데이터를 영구적으로 보간하기 -> Database
# Model -> Database 사용하기 편함
# Security
# Template engine
