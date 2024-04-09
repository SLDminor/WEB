from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Tag, Vote, Answer, Profile
from mimesis import Person, Text
from mimesis.locales import Locale
import random

class Command(BaseCommand):
    help = 'Fill database with randomized content'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for entity population')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        num_profiles = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_votes = ratio * 200

        self._fill_profiles(num_profiles)
        self._fill_tags(num_tags)
        self._fill_questions(num_questions)
        self._fill_answers(num_answers)
        self._fill_votes(num_votes)

    def _fill_profiles(self, num_profiles):
        print(f'Creating {num_profiles} profiles...')
        users = []
        for _ in range(num_profiles):
            person = Person(Locale.EN)
            user = User.objects.create_user(username=person.username(),
                                            email=person.email(),
                                            password=person.password())
            profile = Profile(user=user)
            users.append(profile)
        Profile.objects.bulk_create(users, ignore_conflicts=True)

    def _fill_tags(self, num_tags):
        print(f'Creating {num_tags} tags...')
        tags = []
        for _ in range(num_tags):
            txt = Text(Locale.EN)
            t = Tag(title=txt.word())
            tags.append(t)
        Tag.objects.bulk_create(tags, ignore_conflicts=True)

    def _fill_questions(self, num_questions):
        print(f'Creating {num_questions} questions...')
        users = list(User.objects.all())
        random.shuffle(users)
        questions = []
        for _ in range(num_questions):
            txt = Text(Locale.EN)
            q = Question(title=txt.quote(),
                         body=txt.text(30),
                         author=random.choice(users))
            questions.append(q)
        Question.objects.bulk_create(questions, ignore_conflicts=True)

    def _fill_answers(self, num_answers):
        print(f'Creating {num_answers} answers...')
        users = list(User.objects.all())
        questions = list(Question.objects.all())
        n = 10
        for j in range(n):
            print(f'Creating answers #{j + 1}...')
            answers = []
            for _ in range(num_answers // n):
                txt = Text(Locale.EN)
                a = Answer(body=txt.text(30),
                           author=random.choice(users),
                           question=random.choice(questions),
                           is_correct=False)
                answers.append(a)
            Answer.objects.bulk_create(answers, ignore_conflicts=True)

    def _fill_votes(self, num_votes):
        print(f'Creating {num_votes} votes...')
        random_model_instances = list(Question.objects.all()) + list(Answer.objects.all())
        users = list(User.objects.all())
        n = 500
        for j in range(n):
            print(f'Creating votes #{j + 1}...')
            votes = []
            for _ in range(num_votes // n):
                rates = [-1, 1]
                v = Vote(rate=random.choice(rates),
                         author=random.choice(users),
                         content_object=random.choice(random_model_instances))
                votes.append(v)
            Vote.objects.bulk_create(votes, ignore_conflicts=True)
