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

def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, per_page = 5)
    page_obj = paginator.page(page_num)
    return render(request, template_name="index.html", context= {"questions": page_obj})

def hot(request):
    return render(request, template_name="hot.html", context= {"questions": QUESTIONS})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render (request, template_name='one_question.html', context={'questions': item})
