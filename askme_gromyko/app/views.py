from django.http import Http404
from django.shortcuts import render
from app import views
from django.core.paginator import Paginator

QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(200)
]

ANSWERS = [
{
    "id": i,
    "title": f"Answer {i}",
    "text": f"This is answer number {i}"
} for i in range(3)
]

def index(request):
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
    except ValueError:
        raise Http404("Page number is not valid.")

    paginator = Paginator(QUESTIONS, per_page = 5)
    page_obj = paginator.page(page_num)
    return render(request, template_name="index.html", context= {"questions": page_obj})

def hot(request):
    return render(request, template_name="hot.html", context= {"questions": QUESTIONS})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render (request, template_name='one_question.html', context={'questions': item, 'answers': ANSWERS})

def ask(request):
    return render(request, template_name="ask.html")

def login(request):
    return render(request, template_name="login.html")

def signup(request):
    return render(request, template_name="signup.html")

def settings(request):
    return render(request, template_name="settings.html")

def tag(request):
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
    except ValueError:
        raise Http404("Page number is not valid.")

    paginator = Paginator(QUESTIONS, per_page = 5)
    page_obj = paginator.page(page_num)
    return render(request, template_name="tag_blablabla.html", context= {"questions": page_obj})
