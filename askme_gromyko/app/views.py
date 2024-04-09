from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Tag, Question, Answer


def index(request):
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
    except ValueError:
        raise Http404("Page number is not valid.")

    paginator = Paginator(Question.objects.sorted_by_created_at(), per_page = 5)
    page_obj = paginator.page(page_num)
    global_tags = Tag.objects.sort_by_related_question_quantity()[:9]
    
    return render(request, template_name="index.html", context = {'page_obj': page_obj, 'global_tags': global_tags,})

def hot(request):
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
    except ValueError:
        raise Http404("Page number is not valid.")

    paginator = Paginator(Question.objects.sorted_by_rating(), per_page = 5)
    page_obj = paginator.page(page_num)
    global_tags = Tag.objects.sort_by_related_question_quantity()[:9]
    
    return render(request, template_name="hot.html", context = {'page_obj': page_obj, 'global_tags': global_tags,})

def question(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = Answer.objects.filter(question_id=question_id)
    global_tags = Tag.objects.sort_by_related_question_quantity()[:9]

    return render (request, template_name='one_question.html', context = {'question': question,
                                                                          'global_tags': global_tags,
                                                                          'answers': answers})

def ask(request):
    return render(request, template_name="ask.html")

def login(request):
    return render(request, template_name="login.html")

def signup(request):
    return render(request, template_name="signup.html")

def settings(request):
    return render(request, template_name="settings.html")

def tag(request, title):
    try:
        page_title = str(title)
    except ValueError:
        raise Http404("Page title is not valid.")
    page_obj = Question.objects.filter_by_tag(page_title)
    global_tags = Tag.objects.sort_by_related_question_quantity()[:9]
    tag = Tag.objects.get(title=title)

    return render(request, template_name='show_tag.html', context={
        'page_obj': page_obj,
        'global_tags': global_tags,
        'tag': tag,
    })
