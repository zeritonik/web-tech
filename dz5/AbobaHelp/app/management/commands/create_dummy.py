from django.core.management.base import BaseCommand

from app.models import *

import os
import random

class Command(BaseCommand):
    help = 'Create dummy users'

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int)

    def create_dummy_users(self, count):
        AVATARS = ["img/avatars/" + avatar for avatar in os.listdir("static/img/avatars")]

        start_ind = 1
        while User.objects.filter(username=f"dummy-user-{start_ind}").exists():
            start_ind += 1

        end_ind = start_ind + count
        new_users = User.objects.bulk_create(
            [User(username=f"dummy-user-{i}", password="password") for i in range(start_ind, end_ind)]
        )
        new_profiles = Profile.objects.bulk_create(
            [Profile(user=user, nickname=user.username, avatar=random.choice(AVATARS)) for user in new_users]
        )

        print(f"Created users {start_ind}-{end_ind}")
        return new_profiles

    def create_dummy_tags(self, count):
        start_ind = 1
        while Tag.objects.filter(name=f"dummy-tag-{start_ind}").exists():
            start_ind += 1
        end_ind = start_ind + count
        new_tags = Tag.objects.bulk_create(
            [Tag(name=f"dummy-tag-{i}") for i in range(start_ind, end_ind)]
        )

        print(f"Created tags {start_ind}-{end_ind}")
        return new_tags

    def create_dummy_questions(self, count, profiles, tags):
        start_ind = 1
        while Question.objects.filter(title=f"dummy-question-{start_ind}").exists():
            start_ind += 1

        end_ind = start_ind + count
        new_questions = Question.objects.bulk_create(
            [Question(
                title=f"dummy-question-{i}", 
                text=f"dummy-question-{i} text", 
                author=random.choice(profiles)
            ) for i in range(start_ind, end_ind)]
        )
        for question in new_questions:
            question.tags.add(*random.sample(tags, random.randint(1, min(6, len(tags)))))
        print(f"Created questions {start_ind}-{end_ind}")
        return new_questions

    def create_dummy_answers(self, count, questions, profiles):
        start_ind = 1
        while Answer.objects.filter(text=f"dummy-answer-{start_ind}").exists():
            start_ind += 1

        end_ind = start_ind + count
        new_answers = Answer.objects.bulk_create(
            [Answer(
                text=f"dummy-answer-{i}", 
                author=random.choice(profiles), 
                question=random.choice(questions), 
                correct=random.choice([True, False])
            ) for i in range(start_ind, end_ind)]
        )
        print(f"Created answers {start_ind}-{end_ind}")
        return new_answers

    def create_dummy_likes(self, count, questions, answers, profiles):
        question_likes = random.randint(0, count)
        answer_likes = count - question_likes

        random.shuffle(questions)
        random.shuffle(answers)

        for question in questions:
            if question_likes == 0:
                break
            c = min(question_likes, random.randint(min(len(profiles), question_likes // len(questions)), len(profiles)))
            question_likes -= c
            QuestionLike.objects.bulk_create(
                [QuestionLike(question=question, author=profile, like=random.choice([-1, 1])) for profile in random.sample(profiles, c)]
            )
        
        for answer in answers:
            if answer_likes == 0:
                break
            c = min(answer_likes, random.randint(min(len(profiles), answer_likes // len(answers)), len(profiles)))
            answer_likes -= c
            AnswerLike.objects.bulk_create(
                [AnswerLike(answer=answer, author=profile, like=random.choice([-1, 1])) for profile in random.sample(profiles, c)]
            )

        print(f"Created likes {count}")

    def handle(self, *args, **options):
        try:
            count = options["count"]
            profiles = self.create_dummy_users(count)
            tags = self.create_dummy_tags(count)
            questions = self.create_dummy_questions(count * 10, profiles, tags)
            answers = self.create_dummy_answers(count * 100, questions, profiles)
            self.create_dummy_likes(count * 200, questions, answers, profiles)

            print("Created dummy records")
        except Exception as e:
            print(e)